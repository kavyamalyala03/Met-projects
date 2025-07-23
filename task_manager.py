from fastapi import FastAPI
import json
import sqlite3

def connect_db():
    conn = sqlite3.connect("account.db")
    return conn
 
app = FastAPI()

@app.get("/users")
def read_users():

    conn=connect_db()

    cursor=conn.cursor()

    cursor.execute("SELECT *FROM users")

    data=cursor.fetchall()

    conn.close()

    output=[]

    for entry in data:
        output.append({
            "username": entry[1],
            "password": entry[2],
            "is_login":entry[3]
        })
    return data

@app.post("/signup")
def signup(username,password):
    conn=connect_db()

    cursor=conn.cursor()

    cursor.execute("INSERT INTO users(username,password) VALUES (?,?)",(username,password))
    
    data=cursor.fetchall()

    conn.commit()

    conn.close()

    output=["signup success"]

    for entry in data:
        output.append({
            "username": entry[1],
            "password": entry[2]
        })
    return output

@app.post("/users/login")
def login(username,password):
    conn=connect_db()

    cursor=conn.cursor()

    cursor.execute("SELECT password,is_login FROM users WHERE username=?",(username,))

    r_password= cursor.fetchone()
    if r_password and r_password[0]==password and r_password[1]!=1:
        cursor.execute("UPDATE users SET is_login=? WHERE username=?",(1,username))
        conn.commit()
        conn.close()
        return "login successful"    

    conn.close()
    return "Invalid Username or password"

@app.post("/users/logout")
def logout(username,password):
    conn = connect_db()
    cursor= conn.cursor()
    cursor.execute("SELECT is_login FROM users WHERE username=? AND password=?", (username,password))
    user = cursor.fetchone()
    if user:
        if user[0] == 1:
            cursor.execute("UPDATE users SET is_login = 0 WHERE username=? AND password=?", (username, password))
            conn.commit()
            conn.close()
            return "User logged out successfully"
        else:
            return  "User is not logged in"
    else:
        return  "Invalid username or password"

@app.get("/users/tasks")
def users_tasks(username):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return {"error": "User not found"}

    cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user[0],))
    data= cursor.fetchall()
    conn.close()
    return data


@app.post("/adding/tasks")
def add_tasks(username,title,description):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=?",(username,))
    user=cursor.fetchone()

    if not user:
        conn.close()
        return {"error": "User not found"}
    
    cursor.execute("INSERT INTO tasks(user_id,title,description) VALUES (?,?,?)",(user[0],title,description))
    conn.commit()
    conn.close()
    return "tasks added"

@app.delete("/delete/users/{id}")
def delete(id:int):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?",(id,))
    conn.commit()

    deleted=cursor.rowcount
    conn.close()

    if deleted:
        return "deleted successful"
    else:
        return "unsuccesful" 
    
@app.delete("/delete/tasks/{id}")
def delete(id:int):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?",(id,))
    conn.commit()

    deleted=cursor.rowcount
    conn.close()

    if deleted:
        return "deleted successful"
    else:
        return "unsuccesful"









 