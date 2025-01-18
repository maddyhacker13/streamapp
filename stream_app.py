import os
import streamlit as st
import mysql.connector
from datetime import datetime
from pathlib import Path

# Define the upload folder
UPLOAD_FOLDER = "shared_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MySQL connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="sql12.freemysqlhosting.net", 
            user="sql12758420", 
            password="iuMFynlPbN", 
            database="sql12758420",
            port=3306
        )
        return connection
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

# Save file metadata to the database
def save_to_database(filename, filepath):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO files (filename, filepath, upload_time) VALUES (%s, %s, %s)",
            (filename, filepath, datetime.now())
        )
        connection.commit()
        cursor.close()
        connection.close()

# Fetch files from the database
def get_files_from_database():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, filename, filepath, upload_time FROM files")
        files = cursor.fetchall()
        cursor.close()
        connection.close()
        return files
    return []

# Streamlit app
st.title("File Sharing Web Application 📂")

# File Upload Section
st.header("Upload Your Files")
uploaded_files = st.file_uploader("Select file(s) to upload", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = Path(UPLOAD_FOLDER) / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        save_to_database(uploaded_file.name, str(file_path))
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# File Download Section
st.header("Available Files for Download")
files = get_files_from_database()

if files:
    for file_id, filename, filepath, upload_time in files:
        # Generate a direct download link using the streamlit app domain
        file_url = f"https://streamapp-ezyabtk4e6ipybqgb6aded.streamlit.app/{filepath}"

        st.markdown(f"**{filename}** (Uploaded on {upload_time})")
        st.markdown(f"[Download File]({file_url})", unsafe_allow_html=True)
else:
    st.write("No files uploaded yet.")
