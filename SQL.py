from dotenv import load_dotenv
load_dotenv() # load all the environemnt variables  
import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function To Load Google Gemini Model and provide queries as a response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function To retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name PIZZA and has the following columns - ID, NAME, SIZE, TOPPINGS, PRICE \n\nFor example,
    \nExample 1 - How many entries of pizzas are there?,
    the SQL command will be something like this SELECT COUNT(*) FROM PIZZA ;
    \nExample 2 - Show me all the pizzas with prices less than 15?,
    the SQL command will be something like this SELECT * FROM PIZZA
    WHERE PRICE < 15;
    also, the SQL code should not have ``` in the beginning or end and SQL word in the output
    """
]

# Streamlit App
st.set_page_config(page_title="Unleashing the Power to Fetch Any Query")
st.header("SQL Query Gemini Application")

question = st.text_input("Input: ", key="input")

submit = st.button("ask me anything about pizzas and SQL queries!")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response = read_sql_query(response, "pizza.db")
    st.subheader("The Response is")
    for row in response:
        print(row)
        st.header(row)
