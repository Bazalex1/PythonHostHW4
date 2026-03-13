import pandas as pd
import plotly.express as plt
import requests
import streamlit as strl
import asyncio

API_URL = "https://pythonhosthw4.onrender.com"


strl.set_page_config(page_title='Dashboard', layout="wide")

strl.title("Dashboard streamlit")


def get_records():
    try:
        response = requests.get(f"{API_URL}/records")

    except Exception as e:

        raise Exception(e)

    return response.json()


def add_record(payload: dict):

    return requests.post(f'{API_URL}/records', json=payload, timeout=1)


def delete_record(record_id: int):

    return requests.delete(f"{API_URL}/records/{record_id}", timeout=1)


def load_data() -> pd.DataFrame:
    recrds = get_records()
    table = pd.DataFrame(recrds)
    table = pd.DataFrame(recrds)
    if not table.empty:
        table['timestep'] = pd.to_datetime(table['timestep'])
        table = table.sort_values('timestep').reset_index(drop=True)
    return table


try:
    table = load_data()

except Exception as e:

    strl.error(f'Не удалось загрузить данные: {e}')

    strl.stop()


strl.subheader("Таблица данных")

strl.dataframe(table, width='stretch')


if not table.empty:

    col1, col2 = strl.columns(2)

    with col1:

        fig_consumption = plt.line(
            table,
            x="timestep",
            y=["consumption_eur", "consumption_sib"],
            title="Потребление",
        )

        strl.plotly_chart(fig_consumption)

    with col2:

        fig_price = plt.line(
            table,
            x="timestep",
            y=["price_eur", "price_sib"],
            title="Цены",
        )

        strl.plotly_chart(fig_price)


strl.subheader("Добавить запись")


with strl.form("add_record_form"):

    timestep = strl.text_input("Время")

    consumption_eur = strl.number_input("Потребление EUR", min_value=0.0, step=0.1)

    consumption_sib = strl.number_input("Потребление SIB", min_value=0.0, step=0.1)

    price_eur = strl.number_input("Цена EUR", min_value=0.0, step=0.01)

    price_sib = strl.number_input("Цена SIB", min_value=0.0, step=0.01)

    submit_add = strl.form_submit_button("Добавить")

    if submit_add:

        payload = {
            "timestep": timestep,
            "consumption_eur": float(consumption_eur),
            "consumption_sib": float(consumption_sib),
            "price_eur": float(price_eur),
            "price_sib": float(price_sib),
        }

        response = add_record(payload)

        if response.status_code == 201:

            strl.success("Запись успешно добавлена")
            strl.rerun()

        else:

            try:

                detail = response.json().get("detail", "Ошибка добавления")

            except Exception:

                detail = response.text
            strl.error(detail)


strl.subheader("Удалить запись")


if not table.empty:

    record_id = strl.number_input("ID записи", min_value=1, step=1)

    if strl.button("Удалить запись"):
        response = delete_record(int(record_id))

        if response.status_code == 200:

            strl.success(f"Запись с id={int(record_id)} удалена")
            strl.rerun()

        else:

            try:

                detail = response.json().get("detail", "Ошибка удаления")

            except Exception:

                detail = response.text
            strl.error(detail)

else:

    strl.info("Нет записей для удаления")
