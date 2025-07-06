from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import hashlib

users_db = {
    "alice": hashlib.sha256("password123".encode()).hexdigest(),
    "bob": hashlib.sha256("mypassword".encode()).hexdigest()
}

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    hashed_password_in = hashlib.sha256(password.encode()).hexdigest()

    if users_db.get(username) and users_db[username] == hashed_password_in:
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
    return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid username or password"})

