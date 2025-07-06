from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os, hashlib
# from passlib.context import CryptContext

users = {}

def create_user(username: str, password: str):
    salt = os.urandom(16)
    hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    )

    users[username] = {
        'salt': salt.hex(),
        'hash': hash.hex()
    }

create_user('alice', 'inwonderland')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):

    if users.get(username) is None:
        return templates.TemplateResponse("login.html", {"request": request, "message": "User not found"})
    
    salt = users[username]['salt']
    hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        bytes.fromhex(salt),
        100000
    ).hex()

    if hash == users[username]['hash']:
        return templates.TemplateResponse("welcome.html", {"request": request, "username": username})
    return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid password"})