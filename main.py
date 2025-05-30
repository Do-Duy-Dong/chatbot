from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn
from langchain_huggingface import HuggingFaceEmbeddings
import test
import os
app=FastAPI()
embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

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