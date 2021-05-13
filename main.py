import sqlite3
from config import *
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    connection = sqlite3.connect(DB_FILE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    #gets data from DB
    cursor.execute("""
        SELECT symbol, name FROM stock ORDER BY symbol
    """)

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})
    


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    connection = sqlite3.connect(DB_FILE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    #gets data from DB
    cursor.execute("""
        SELECT id, symbol, name FROM stock WHERE symbol = ?
    """, (symbol,))

    row = cursor.fetchone()


    cursor.execute("""
        SELECT * FROM stock_price WHERE stock_id = ?
    """, (row['id'],))

    prices = cursor.fetchall()
    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})
