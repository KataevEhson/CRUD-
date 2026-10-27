from conection import *





async def create_user_by_id(full_name, username, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
INSERT INTO users (full_name, user_name, tg_id) VALUES
($1, $2, $3)
""", full_name, username, str(tg_id))
    except Exception as erorr:
        print("Create user erorr:", erorr)
    finally:
        await conn.close()





async def create_task_by_id(title, caption, due_date, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
INSERT INTO tasks (title, caption, due_date, tg_id) VALUES
($1, $2, $3, $4)
""", title, caption, due_date, str(tg_id))
    except Exception as erorr:
        print("Create task erorr:", erorr)

    finally:
        await conn.close()







async def for_for_read(task_id, tg_id):
    try:
        conn = await connection_db()
        a1 = await conn.fetch("""
SELECT * FROM tasks
where id = $1 and tg_id = $2
""", task_id, str(tg_id))
        return a1
    except Exception as erorr:
        print(f"Show your task erorr {erorr}")
    finally:
        await conn.close()






async def update_table_by_id(title, caption, due_date, task_id, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
UPDATE tasks
SET title = $1,
caption = $2,
due_date = $3
WHERE id = $4 and tg_id = $5
""", title, caption, due_date, task_id, str(tg_id) )
    except Exception as erorr:
        print("Update task erorr:", erorr)
    finally:
        await conn.close()    






async def drop_task(task_id, tg_id):
    try:
        conn = await connection_db()
        await conn.execute("""
DELETE FROM tasks
WHERE id = $1 and tg_id = $2
""", task_id, str(tg_id))
    except Exception as rorr:
        print("Drop task erorr:", rorr)
    finally:
        await conn.close()