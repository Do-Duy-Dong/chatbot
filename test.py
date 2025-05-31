#! D:\CodeWeb\bt\myenv\Scripts\python.exe
import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
import json
import PyPDF2 as pdf
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
# texts="""Website nhắn tin Snap là một nền tảng trực tuyến cho phép người dùng gửi và nhận tin nhắn theo thời gian thực thông qua kết nối Internet. Hệ thống thường bao gồm các chức năng như đăng nhập, quản lý danh sách bạn bè, trò chuyện 1-1 hoặc nhóm, thông báo khi có tin nhắn mới và lưu trữ lịch sử trò chuyện. Việc xây dựng website nhắn tin giúp tăng khả năng tương tác, hỗ trợ liên lạc nhanh chóng.
# Người làm ra website này là Đỗ Duy Đông.
# Website có tên là Snap."""
# chunk=texts.split("\n")
embedding_model= GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv('GEMINI_KEY'))
def create_vectordb(embedding_model):
    # with open("./document/code.json.txt","r",encoding='utf-8') as f:
    #     data=pdf.PdfReader(f)
    #     for page in data.pages:
    #         chunk=page.split('\n')
    #     db=FAISS.from_texts(texts=chunk,embedding=embedding_model)
    #     db.save_local('./dbvector/faiss_index2')
    db= FAISS.from_texts(texts=chunk,embedding=embedding_model)
    db.save_local('./dbvector/faiss_index3')
    print('success')
def add_text_to_vectordb(texts,embedding_model):
    db=FAISS.load_local('./dbvector/faiss_index',embedding_model,allow_dangerous_deserialization=True)
    db.add_texts(texts)
    db.save_local('./dbvector/faiss_index')

def search_vector(query,embedding_model):
    db=FAISS.load_local('./dbvector/faiss_index3',embedding_model,allow_dangerous_deserialization=True)
    result=db.similarity_search(query,k=3)
    return result

def answer(result,query):
    config= genai.types.GenerationConfig(temperature=0,max_output_tokens=500)
    # prompt2= f'Giả sử bạn là trợ lý ảo tư vấn món ăn cho website nhà hàng A2Restuarant của tôi, hãy trả lời câu hỏi được khách hàng đưa ra,sử dụng dữ liệu này {result} để trả lời, nếu không biết thì hãy trả lời kiểu câu hỏi nằm ngoài dữ liệu của tôi.Câu hỏi của khách:"{query}"'
    promt3=f'Giả sử bạn là chatbot nhắn tin cho website Snap nhắn tin của tôi, hãy trả lới câu hỏi được người dùng đưa ra dựa trên dữ liệu này {result}, nếu nằm ngoài dữ liệu kia thì bạn hãy tự trả lời bằng kiến thức của bạn, không trả lời kiểu dựa vào dữ liệu hay dữ liệu không cung cấp.Câu hỏi của người dùng:"{query}"'
    # genai.configure(api_key=os.getenv('GEMINI_KEY'))
    model= genai.GenerativeModel('gemini-1.5-flash')
    response1=model.generate_content(contents=promt3,generation_config=config)
    return response1.text
result=search_vector('Ai làm ra website này',embedding_model)
print(result)