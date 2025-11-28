from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse 
import mysql.connector
from configuration.conections import DatabaseConnection
import os
from service.openweathermap_service import get_meterological_data

API_KEY_OpenWeatherMap = os.getenv("API_KEY_OpenWeatherMap")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}

@app.get("/users")
def read_users():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tatoch2001!",
        database="pruebadb"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    data = mycursor.fetchall()
    mydb.close()
    return data

@app.post("/users")
async def post_user(request: Request):
    mydb=DatabaseConnection(
        host="localhost",
        user="root",
        password="Tatoch2001!",
        database="pruebadb"
    )
    mydb_conn = await mydb.get_connection()
    body = await request.json()
    username= body['username']
    age= body['age']
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"INSERT INTO users (username, age) VALUES ('{username}', {age})")
    mydb_conn.commit()
    return JSONResponse(content={"message": "User added successfully"}, status_code=201)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    mydb=DatabaseConnection(
        host="localhost",
        user="root",
        password="Tatoch2001!",
        database="pruebadb"
    )
    mydb_conn = await mydb.get_connection()
    mycursor = mydb_conn.cursor()
    mycursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = mycursor.fetchone()
    mydb_conn.close()
    if user:
        return {"id": user[0], "username": user[1], "age": user[2]}
    else:
        return JSONResponse(content={"message": "User not found"}, status_code=404)
    
@app.get("/weather/{city}")
async def get_weather(city: str):
    weather_data = get_meterological_data(city, API_KEY_OpenWeatherMap)
    if "error" in weather_data:
        raise HTTPException(status_code=404, detail="City not found")
    return JSONResponse(content=weather_data, status_code=200)