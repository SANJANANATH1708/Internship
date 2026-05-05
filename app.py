import streamlit as st
import pandas as pd
import datetime

def log_event():
    with open("log.txt", "a") as f:
        f.write(f"Login at {datetime.datetime.now()}\n")

# -------------------------------
# BASIC LOGIN
# -------------------------------
st.title("📊 Internship Dashboard Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")


if username == "admin" and password == "1234":
    st.success("Login Successful")

    log_event()   # 👈 ADD THIS LINE

    st.title("📊 Sales Dashboard")

    df = pd.read_csv("outputs/category_month_summary.csv")

    st.write("Data Preview")
    st.dataframe(df)

    st.line_chart(df.select_dtypes(include='number'))

else:
    st.warning("Enter valid login details")

import datetime

def log_event():
    with open("log.txt", "a") as f:
        f.write(f"Login at {datetime.datetime.now()}\n")

# call it after login success
log_event()