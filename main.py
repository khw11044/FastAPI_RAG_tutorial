import os 
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import bs4
import traceback
from pydantic import BaseModel

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load environment variables 
load_dotenv()


app = FastAPI()

#  CORS 정책에 의해 요청이 거부되는 것을 막는다
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # FastAPI에 CORS 예외 URL을 등록하여 해결
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일들 (html, css 등)에 접근
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenAI API 키는 .env 파일에서 관리합니다.
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# 임베딩모델과 llm 선정
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
llm = ChatOpenAI(openai_api_key=openai_api_key, model = "gpt-4o-mini")

# pydantic의 BaseModel로 클래서 선언 
# url은 str로 받아옴, URL 입력
class URLInput(BaseModel):
    url: str

# query은 str로 받아옴, 질문 입력 
class QueryInput(BaseModel):
    query: str

# 전역 변수로 RAG 체인을 관리합니다.
rag_chain = None


# FastAPI 구성 
'''
- get("/")
- post("/process_url")
- post("/query")
'''




# 루트 페이지에서는 static/index.html을 불러옴 
@app.get("/")
async def root():                                   # 비동기처리: 여러 사용자들이 한꺼번에 홈페이지에 들어오더라도 여러가지 작업을 한꺼번에 처리할 수 있게 해줌 
    return FileResponse('static/index.html')

# 사용자가 입력한 값을 가지고 처리
# 주어진 url에 대해 RAG를 생성함 
@app.post("/process_url")
async def process_url(url_input: URLInput):     # URLInput으로 사용자의 입력받음 
    global rag_chain
    try:
        loader = WebBaseLoader(
            web_paths=(url_input.url,),
            bs_kwargs=dict(),
        )
        docs = loader.load()
        # print(docs)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return {"message": "URL processed successfully"}
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in process_url: {error_trace}")
        raise HTTPException(status_code=500, detail=str(e))

# 사용자가 쿼리를 입력하였을 때 처리 
@app.post("/query")
async def query(query_input: QueryInput):       # QueryInput으로 사용자의 입력받음 
    global rag_chain
    if not rag_chain:
        raise HTTPException(status_code=400, detail="Please process a URL first")
    try:
        result = rag_chain.invoke({"input": query_input.query})
        return {"answer": result["answer"]}
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in query: {error_trace}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


