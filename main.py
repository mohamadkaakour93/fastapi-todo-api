from fastapi import FastAPI, HTTPException, Header, Depends
import sqlite3

app = FastAPI()

# Connexion DB
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

# Création table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    completed BOOLEAN
)
""")
conn.commit()


def verify_token(token: str = Header(None)):
    if token != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token


@app.get("/")
def root():
    return {"message": "API FastAPI OK"}


@app.get("/tasks", dependencies=[Depends(verify_token)])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "completed": bool(row[3])
        })

    return tasks


@app.post("/tasks", dependencies=[Depends(verify_token)])
def create_task(task: dict):
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (task["title"], task["description"], task["completed"])
    )
    conn.commit()

    return {"message": "Task created"}


@app.get("/tasks/{task_id}", dependencies=[Depends(verify_token)])
def get_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "completed": bool(row[3])
    }


@app.put("/tasks/{task_id}", dependencies=[Depends(verify_token)])
def update_task(task_id: int, updated_task: dict):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
        (updated_task["title"], updated_task["description"], updated_task["completed"], task_id)
    )
    conn.commit()

    return {"message": "Task updated"}


@app.delete("/tasks/{task_id}", dependencies=[Depends(verify_token)])
def delete_task(task_id: int):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Task not found")

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

    return {"message": "Task deleted"}