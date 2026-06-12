from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import get_connection, create_table

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def startup():
    create_table()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.post("/book")
def book_room(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    check_in: str = Form(...),
    check_out: str = Form(...),
    room_type: str = Form(...),
    guests: int = Form(...),
    special_requests: str = Form("")
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bookings (full_name, email, phone, check_in, check_out, room_type, guests, special_requests)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (full_name, email, phone, check_in, check_out, room_type, guests, special_requests))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Booking successful!", "name": full_name}