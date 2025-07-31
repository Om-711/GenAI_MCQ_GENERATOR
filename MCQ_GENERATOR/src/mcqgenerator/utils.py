import os
import PyPDF2
import json
import traceback

import os
import PyPDF2
import json
import traceback

# def read_file(file):
#     if file.name.endswith(".pdf"):
#         try:
#             pdf_reader=PyPDF2.PdfFileReader(file)
#             text=""
#             for page in pdf_reader.pages:
#                 text+=page.extract_text()
#             return text
            
#         except Exception as e:
#             raise Exception("Why Error reading the PDF file")
        
#     elif file.name.endswith(".txt"):
#         return file.read().decode("utf-8")
    
#     else:
#         raise Exception(
#             "unsupported file format only pdf and text file suppoted"
#             )
# import PyPDF2
from io import BytesIO

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            file_bytes = BytesIO(file.read())  # Convert UploadedFile to BytesIO
            pdf_reader = PyPDF2.PdfReader(file_bytes)  # Use PyPDF2.PdfReader not PdfFileReader (deprecated)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

        elif file.name.endswith(".txt"):
            return file.read().decode("utf-8")

        else:
            raise Exception("Unsupported file format. Only PDF and TXT are supported.")

    except Exception as e:
        raise Exception(f"Error reading the file: {str(e)}")

def get_table_data(quiz_str):
    try:
        quiz_dict=json.loads(quiz_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
            
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

