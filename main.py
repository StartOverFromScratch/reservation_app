from fastapi import FastAPI, Request, Form
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        equipment TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/reservations")
async def get_reservations():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM reservations")
    data = [dict(zip(["id", "name", "equipment", "start_date", "end_date"], row)) for row in c.fetchall()]
    conn.close()
    return data

@app.post("/api/reservations")
async def create_reservation(name: str = Form(...), equipment: str = Form(...), start_date: str = Form(...), end_date: str = Form(...)):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO reservations (name, equipment, start_date, end_date) VALUES (?, ?, ?, ?)", (name, equipment, start_date, end_date))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.put("/api/reservations/{reservation_id}")
async def update_reservation(reservation_id: int, request: Request):
    data = await request.json()
    name = data.get("name")
    equipment = data.get("equipment")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        UPDATE reservations
        SET name=?, equipment=?, start_date=?, end_date=?
        WHERE id=?
    """, (name, equipment, start_date, end_date, reservation_id))
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="予約が見つかりません")
    conn.close()
    return {"status": "updated"}

@app.delete("/api/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
    conn.commit()
    if c.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="予約が見つかりません")
    conn.close()
    return {"status": "deleted"}