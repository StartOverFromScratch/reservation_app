from fastapi import FastAPI, Request, Form
from fastapi import HTTPException
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import Reservation, Equipment, Category
from database import engine, SessionLocal
from datetime import datetime


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/reservations")
async def get_reservations():
    db: Session = SessionLocal()
    reservations = db.query(Reservation).options(joinedload(Reservation.equipment)).all()
    data = []
    for r in reservations:
        data.append({
            "id": r.id,
            "name": r.user_name,
            "equipment": r.equipment.name if r.equipment else "不明",
            "start_date": r.start_time.strftime("%Y-%m-%d"),
            "end_date": r.end_time.strftime("%Y-%m-%d")
        })
    db.close()
    return data

@app.post("/api/reservations")
async def create_reservation(name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    equipment_id: int = Form(...)
):
    try:
        db : Session = SessionLocal()
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        reservation = Reservation(
            user_name=name,
            start_time=start,
            end_time=end,
            equipment_id=equipment_id
        )
        db.add(reservation)
        db.commit()
        db.close()
        return {"status": "success"}
    
    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail=f"予約登録に失敗しました: {e}")

    finally:
        db.close()
        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.put("/api/reservations/{reservation_id}")
async def update_reservation(reservation_id: int, request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    name = data.get("name")
    equipment_id = data.get("equipment")  # IDを受け取る前提
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="予約が見つかりません")

    reservation.user_name = name
    reservation.equipment_id = equipment_id
    reservation.start_time = datetime.fromisoformat(start_date)
    reservation.end_time = datetime.fromisoformat(end_date)

    db.commit()
    return {"status": "updated"}

@app.delete("/api/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="予約が見つかりません")

    db.delete(reservation)
    db.commit()
    return {"status": "deleted"}

@app.get("/api/categories")
def get_categories():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, name FROM categories")
    categories = [{"id": row[0], "name": row[1]} for row in c.fetchall()]
    conn.close()
    return categories

@app.post("/api/categories")
def create_category(data: dict):
    name = data.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Category name is required")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return {"message": "Category created"}

@app.get("/api/equipments")
def get_equipment():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        SELECT equipment.id, equipment.name, categories.id, categories.name
        FROM equipment
        LEFT JOIN categories ON equipment.category_id = categories.id
    """)
    equipments = []
    for row in c.fetchall():
        equipments.append({
            "id": row[0],
            "name": row[1],
            "category_id": row[2],
            "category_name": row[3]
        })
    conn.close()
    return equipments

@app.post("/api/equipments")
def create_equipments(data: dict):
    name = data.get("name")
    category_id = data.get("category_id")
    if not name or category_id is None:
        raise HTTPException(status_code=400, detail="Equipment name and category_id are required")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO equipment (name, category_id) VALUES (?, ?)", (name, category_id))
    conn.commit()
    conn.close()
    return {"message": "Equipment created"}