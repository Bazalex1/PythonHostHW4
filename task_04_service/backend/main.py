from pathlib import Path

from typing import List


from fastapi import FastAPI, HTTPException, status

from pydantic import BaseModel, Field, field_validator
import pandas as pd

import asyncio


app = FastAPI(title='Dashboad API')


BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "data.csv"


columns = [
    "id",
    "timestep",
    "consumption_eur",
    "consumption_sib",
    "price_eur",
    "price_sib",
]


file_lock = asyncio.Lock()


class CreateRecord(BaseModel):
    timestep: str

    consumption_eur: float = Field()

    consumption_sib: float = Field()

    price_eur: float = Field()

    price_sib: float = Field()

    @field_validator('timestep')
    @classmethod
    def val_timestep(clas, value: str) -> str:

        try:
            date = pd.to_datetime(value)
            return date.strftime('%Y-%m-%d %H:%M')
        except ValueError:

            raise ValueError('Формат должен быть %Y-%m-%d %H:%M')


class Record(CreateRecord):
    id: int


def write_data(table: pd.DataFrame) -> None:

    table.to_csv(DATA, index=False)


def read_csv() -> pd.DataFrame:

    if not DATA.exists():

        raise ValueError('Поместите файл data.csv в папку backend')

    table = pd.read_csv(DATA)

    if table.empty:

        raise ValueError('файл data.csv пустой')

    if "id" not in table.columns:
        table.insert(0, "id", range(1, len(table) + 1))
        write_data(table)

    return table


async def load_data() -> pd.DataFrame:

    return await asyncio.to_thread(read_csv)


async def save_data(table: pd.DataFrame) -> None:

    await asyncio.to_thread(write_data, table)


@app.get("/records", response_model=List[Record])
async def get_records():

    try:

        async with file_lock:

            table = await load_data()

            table = table.sort_values('timestep').reset_index(drop=True)

        return table.to_dict(orient='records')

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Проблема с загрузкой записей {str(e)}',
        )


@app.post("/records", response_model=Record, status_code=status.HTTP_201_CREATED)
async def add_record(record: CreateRecord):

    try:

        async with file_lock:

            table = await load_data()

            if table.empty:

                new_id = 1
            else:

                new_id = int(table['id'].max()) + 1

            new = {
                "id": new_id,
                "timestep": record.timestep,
                "consumption_eur": record.consumption_eur,
                "consumption_sib": record.consumption_sib,
                "price_eur": record.price_eur,
                "price_sib": record.price_sib,
            }

            table = pd.concat([table, pd.DataFrame([new])], ignore_index=True)

            await save_data(table)

        return new

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Не получилось добавить запись {str(e)}',
        )


@app.delete("/records/{record_id}")
async def delete_record(record_id: int) -> dict:

    try:

        async with file_lock:

            table = await load_data()

            if table.empty or record_id not in table['id'].values:

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Запись с таким ID не обнаружена',
                )

            table = table[table['id'] != record_id].copy()

            await save_data(table)

        return {'record': f'Запись {record_id} удалена'}

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Не получилось удалить запись {str(e)}',
        )
