import streamlit as st
import json
import requests

st.title("TASK MANAGEMENT SYSTEM")

API="http://127.0.0.1:8000"
# getting all users
st.subheader("Getting users")
is_getting_users=st.button("Get users",type="secondary")
if is_getting_users:
    response=requests.get(f"{API}/users")
    data=response.json()
    st.dataframe(data)


st.subheader("Create Account For User")
username=st.text_input("**enter username**",placeholder="username")
password=st.text_input("**enter password**",placeholder="password")

is_click_signup=st.sidebar.button("signup",type="primary")
is_click_login=st.sidebar.button("login",type="primary")
is_click_logout=st.sidebar.button("logout",type="primary")

#for signup
if is_click_signup:
    if username and password:
        response=requests.post(f"{API}/signup",params={"username":username,"password":password})
        data=response.json()
        st.write(data)

#for login
if is_click_login:
    if username and password:
        response=requests.post(f"{API}/users/login",params={"username":username,"password":password})
        data=response.json()
        st.write(data)

# for logout
if is_click_logout:
    if username and password:
        response=requests.post(f"{API}/users/logout",params={"username":username,"password":password})
        data=response.json()
        st.write(data)

# for adding tasks
st.subheader("Adding TASKS")
is_click_adding_task=st.sidebar.button("add task",type="primary")
username=st.text_input("**enter username**",placeholder="username",key="username_input")
title=st.text_input("**enter title**",placeholder="title",key="title_input")
description=st.text_input("**enter description**",placeholder="description",key="description_input")

if is_click_adding_task:
    if username and title and description:
        response=requests.post(f"{API}/adding/tasks", params={"username":username,"title":title,"description":description})
        data=response.json()
        st.write(data)

# getting users and tasks
st.subheader("Getting users and tasks")
is_click_get_users_tasks=st.sidebar.button("get users and tasks",type="primary")
username=st.text_input("**enter username**",placeholder="username",key="get_tasks_username")
if is_click_get_users_tasks:
    response=requests.get(f"{API}/users/tasks",params={"username":username})
    data=response.json()
    st.table(data)

# delete users
st.subheader("Delete users")
is_click_delete_user=st.sidebar.button("Delete users",type="primary")
id=st.text_input("**enter id**",placeholder="enter id")
if is_click_delete_user:
    response=requests.delete(f"{API}/delete/users/{id}")
    data=response.json()
    st.write(data)
     
#delete tasks
st.subheader("Delete tasks")
is_click_delete_task=st.sidebar.button("Delete tasks",type="primary")
id=st.text_input("**enter id**",placeholder="enter id",key="delete_id")
if is_click_delete_task:
    response=requests.delete(f"{API}/delete/tasks/{id}")
    data=response.json()
    st.write(data)



 





