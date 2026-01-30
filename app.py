import streamlit as st
import sqlite3
import pandas as pd

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, status TEXT)''')
    conn.commit()
    return conn

conn = init_db()
cursor = conn.cursor()

# --- APP UI ---
st.title("📝 Simple CRUD Task Manager")

menu = ["Create", "Read", "Update", "Delete"]
choice = st.sidebar.selectbox("Navigation", menu)

# --- CREATE ---
if choice == "Create":
    st.subheader("Add a New Task")
    new_task = st.text_input("Task Description")
    status = st.selectbox("Status", ["To Do", "In Progress", "Done"])
    
    if st.button("Add Task"):
        cursor.execute('INSERT INTO tasks (task, status) VALUES (?,?)', (new_task, status))
        conn.commit()
        st.success(f"Added: {new_task}")

# --- READ ---
elif choice == "Read":
    st.subheader("View All Tasks")
    cursor.execute('SELECT * FROM tasks')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Task', 'Status'])
    st.dataframe(df, use_container_width=True)

# --- UPDATE ---
elif choice == "Update":
    st.subheader("Edit a Task")
    cursor.execute('SELECT id, task FROM tasks')
    list_of_tasks = cursor.fetchall()
    task_dict = {t[1]: t[0] for t in list_of_tasks}
    
    selected_task = st.selectbox("Select Task to Edit", list(task_dict.keys()))
    new_status = st.selectbox("Update Status", ["To Do", "In Progress", "Done"])
    
    if st.button("Update"):
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_dict[selected_task]))
        conn.commit()
        st.info(f"Updated {selected_task} to {new_status}")

# --- DELETE ---
elif choice == "Delete":
    st.subheader("Remove a Task")
    cursor.execute('SELECT id, task FROM tasks')
    list_of_tasks = cursor.fetchall()
    task_dict = {t[1]: t[0] for t in list_of_tasks}
    
    task_to_delete = st.selectbox("Select Task to Delete", list(task_dict.keys()))
    
    if st.button("Delete"):
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_dict[task_to_delete],))
        conn.commit()
        st.warning(f"Deleted: {task_to_delete}")