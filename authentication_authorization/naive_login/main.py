from fastapi import FastAPI, Request, Form
from  fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

user = {
    "username": "admin",
    "password": "password"
}


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": "Please log in to continue."})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    stored_username = user.get("username")
    stored_password = user.get("password")
    if username != stored_username or password != stored_password:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Invalid username or password."})
    return templates.TemplateResponse("welcome.html", {"request": request, "username": username})