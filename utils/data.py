import sqlite3

from hashlib import sha256
import random


conn = sqlite3.connect("database/db.db")
cursor = conn.cursor()

async def get_logged_user(tg_id: int) -> bool:
    cursor.execute(f"SELECT id FROM logged WHERE tg_id={tg_id}")
    acc_id = cursor.fetchone()
    if acc_id is None:
        return False
    else:
        return True

async def get_logging_user(login: str, password: str, tg_id: int) -> bool:
    cursor.execute(f"SELECT id, password FROM users WHERE login='{login}'")
    data_user = cursor.fetchone()
    if not data_user is None:
        password_data = data_user[1]
        if str(sha256(password.encode("utf-8")).hexdigest()) == str(password_data):
            await set_logged(data_user[0], tg_id)
            return True
    return False

async def set_logged(user_id: int, tg_id: int) -> None:
    cursor.execute(f"INSERT INTO logged VALUES ({user_id}, {tg_id})")
    conn.commit()

async def create_user(tg_id: int, login: str, password: str) -> bool:
    password = str(sha256(password.encode("utf-8")).hexdigest())
    cursor.execute(f"SELECT id FROM users WHERE login='{login}'")
    data_user = cursor.fetchone()
    if data_user is None:
        while True:
            user_id = random.randint(10000000, 99999999)
            cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
            user = cursor.fetchone()
            if user is None:
                break
        cursor.execute(f"INSERT INTO users VALUES ({user_id}, {tg_id}, '{login}', '{password}')")
        conn.commit()
        await set_logged(1, tg_id)
        return True
    return False

async def delete_session(tg_id: int) -> None:
    cursor.execute(f"DELETE FROM logged WHERE tg_id={tg_id}")
    conn.commit()

async def get_user_ticket_info(series_number: int) -> dict:
    cursor.execute(f"SELECT train, van, place FROM tickets WHERE series_number={series_number} ORDER BY id DESC LIMIT 1")
    user = cursor.fetchone()
    print(user)
    if not user is None:
        data = {"train": user[0], "van": user[1], "place": user[2]}
        return data

async def get_user_id(tg_id: int) -> int:
    cursor.execute(f"SELECT id FROM logged WHERE tg_id={tg_id}")
    user_id = cursor.fetchone()[0]
    return user_id

async def set_pay_order(user_id: int) -> None:
    cursor.execute(f"UPDATE orders SET payment=1 WHERE id={user_id}")
    conn.commit()