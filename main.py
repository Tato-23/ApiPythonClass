from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse 
import mysql.connector
from configuration.conections import DatabaseConnection

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
