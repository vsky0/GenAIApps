import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf 

from dotenv import load_dotenv

load_dotenv() #load env variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

# 
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""

    for page in reader(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text

#prompt template

input_prompt = """

Hey Gemini act like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data sciene, data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job markeet is very competitive and you should provide best assitancce for improving resumes.
Assign the percentage matching based on Job Description and the missing key words with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%", "Missing Keywords:[]", "Profile Summary":""}}
"""

#Streamlit app
st.title("Smart ATS")
st.text("Improve your Resume ATS")

jd = st.text_area("Paste the JD")

uploaded_file = st.file_uploader("Upload ur Resume", type = "pdf", help="please uplpad pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(text)
        st.subheader(response)


