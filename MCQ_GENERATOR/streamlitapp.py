import os
import json
import pandas as pd
from datetime import datetime
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.loggers import logging
from dotenv import load_dotenv
import streamlit as st
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain
from src.mcqgenerator.loggers import logging


with open("response.json", "r") as file:
    response_json = json.load(file)

st.title("MCQ Generator")

with st.form("mcq_form"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    number = st.number_input("Number of questions:", min_value=1, max_value=100, value=5)
    subject = st.text_input("Subject:")
    tone = st.selectbox("Tone:", ["Formal", "Informal", "Neutral"])
    
    submit_button = st.form_submit_button(label="Generate Quiz")

    if submit_button and uploaded_file is not None:
        with st.spinner("Reading file...."):
            try:
                text = read_file(uploaded_file)

                response = generate_evaluate_chain.invoke({
                "text": text,
                "number":5,
                "subject": "Deep learning",
                "tone":"simple",
                "response_json":json.dumps(response_json, indent=4)
            })
                st.write(response.get("quiz"))
                  
            except Exception as e:
                st.error(f"Error reading file: {e}")
                logging.error(f"Error reading file: {e}")
                st.stop()

            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz")
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index += 1
                            st.table(df)
                            st.text_area("Quiz Review", value=response.get("review", ""), height=200)
                        else:
                            st.error("No quiz data found.")
                            logging.error("No quiz data found.")


                else:
                    st.write(response)