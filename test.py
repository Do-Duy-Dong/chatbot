#! D:\CodeWeb\bt\myenv\Scripts\python.exe
import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
import json
import PyPDF2 as pdf
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

def create_vectordb(embedding_model):
    with open("./document/code.json.txt","r",encoding='utf-8') as f:
        data=pdf.PdfReader(f)
        for page in data.pages:
            chunk=page.split('\n')
        db=FAISS.from_texts(texts=chunk,embedding=embedding_model)
        db.save_local('./dbvector/faiss_index3')

def add_text_to_vectordb(texts,embedding_model):
    db=FAISS.load_local('./dbvector/faiss_index3',embedding_model,allow_dangerous_deserialization=True)
    db.add_texts(texts)
    db.save_local('./dbvector/faiss_index3')

def search_vector(query,embedding_model):
    db=FAISS.load_local('./dbvector/faiss_index3',embedding_model,allow_dangerous_deserialization=True)
    result=db.similarity_search(query,k=3)
    return result

def answer(result,query):
    config= genai.types.GenerationConfig(temperature=0,max_output_tokens=500)
    promt3=f'Giả sử bạn là chatbot nhắn tin cho website Snap nhắn tin của tôi, hãy trả lới câu hỏi được người dùng đưa ra dựa trên dữ liệu này {result}, nếu nằm ngoài dữ liệu kia thì bạn hãy tự trả lời bằng kiến thức của bạn, không trả lời kiểu dựa vào dữ liệu hay dữ liệu không cung cấp.Câu hỏi của người dùng:"{query}"'
    genai.configure(api_key=os.getenv('GEMINI_KEY'))
    model= genai.GenerativeModel('gemini-1.5-flash')
    response1=model.generate_content(contents=promt3,generation_config=config)
    return response1.text
