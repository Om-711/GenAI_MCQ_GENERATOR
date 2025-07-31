import os
import json
import traceback
import pandas as pd
from datetime import datetime
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.loggers import logging


from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


import getpass
import os

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

TEMPLATE = """
text : {text}
You are an expert in making quizzes.Given the text above, generate a quiz with {number} questions on the topic of {subject}.
The quiz should be in the {tone} tone.Make Sure questions should not be repeated.Make sure to format your response your format like RESPONSE_JSON below and use
it as a guide.
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template = TEMPLATE
    )

quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)
# quiz_chain = quiz_generation_prompt | llm


TEMPLATE2 = """
You are an expert in english grammarian and writer. Given a Multiple Choice Quiz (MCQ) for {subject} students.You need to
evaluare the quiz  question complexeity and give a complete analysis of the quiz.Only use atmost 30 words to describe the complexeity of quiz
update the quiz question which needs to be change the tone such that it perfectly fits the statement abilities
Quiz MCQs {quiz}. 

Check from an expert of the above quiz
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["quiz", "subject"],
    template=TEMPLATE2)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)





generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)