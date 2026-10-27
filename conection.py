from dotenv import load_dotenv
import asyncpg
import os





load_dotenv()



paswprd_db = os.getenv("PASSWORD_DB")






async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="today_lesson",
            password=paswprd_db
        )
        return conn
    except Exception as Error:
        print(f"Connection Error: {Error}")
        raise





async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
Create table if not exists users(
    id serial primary key,
    full_name varchar(30),
    user_name varchar(30),
    tg_id varchar(30),
    created_at timestamp default now(),
    is_active boolean default true
    );


Create table if not exists tasks(
    id serial primary key,
    title varchar(30),
    caption text,
    due_date varchar(20),
    tg_id varchar(20),
    created_at timestamp default now(),
    is_active boolean default true
    )
""")
        print("Table create sucessful")
    except Exception as erorr:
        print("Create table erorr", erorr)
    finally:
        await conn.close()

1