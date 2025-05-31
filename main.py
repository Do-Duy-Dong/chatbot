from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import test
import os
from dotenv import load_dotenv

load_dotenv()
app=FastAPI()
# embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embedding_model= GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv('GEMINI_KEY'))

class Message(BaseModel):
    message: str

@app.post('/home/chatbot')
async def call_chat(msg: Message):
    result=test.search_vector(msg.message,embedding_model)
    answer=test.answer(result,msg.message)
    return {"reply": f"{answer}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)