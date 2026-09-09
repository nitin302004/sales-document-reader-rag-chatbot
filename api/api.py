import json
import os

import uvicorn
from dotenv import load_dotenv
load_dotenv("/Users/nitin/Downloads/sales_document_reader_chatbot/.env", override=True)
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from pydantic import BaseModel

from api.graph_builder import build_graph
from api.nodes.pdf_processing import get_vector_store
from api.utils.state import State


app = FastAPI(
    title="Sales Document Reader API",
    description="API for extracting and querying information from sales documents.",
    version="1.0.0",
)




global_state: State = {
    "messages": [],
    "contents": b"",
    "file_type": "",
    "dict_return": {},
    "file_path": "",
    "memory": {},
}


class QuestionRequest(BaseModel):
    question: str


@app.post("/chat")
async def ask_question(request: QuestionRequest):
    """
    Answer questions about the uploaded sales PDF
    using the Chroma vector store and RAG.
    """

    print("Inside /chat:", request)

    question = request.question

    # Get the existing vector store
    vector_store = get_vector_store()

    if isinstance(vector_store, str) or vector_store is None:
        raise HTTPException(
            status_code=400,
            detail="Vector store not initialized. Please upload a PDF first.",
        )

    llm = ChatOpenAI()

    prompt = ChatPromptTemplate.from_template(
        """
        You are a sales document analysis assistant.

        Answer the following question using only the
        information available in the provided document context.

        If the answer cannot be found in the context,
        clearly say that the information is not available
        in the uploaded document.

        <context>
        {context}
        </context>

        Question: {input}
        """
    )

    docs_chain = create_stuff_documents_chain(llm, prompt)

    retrieval_chain = create_retrieval_chain(
        vector_store.as_retriever(),
        docs_chain,
    )

    results = retrieval_chain.invoke(
        {"input": question}
    )

    response = {
        "question": question,
        "answer": results["answer"],
    }

    print(response)

    return response


@app.post("/sales")
async def upload_file(file: UploadFile = File(...)):
    """
    Process an uploaded sales document.

    Supported formats:
    - PDF
    - TXT
    - DOCX
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    file_ext = file.filename.split(".")[-1].lower()

    supported_extensions = {"pdf", "txt", "docx"}

    if file_ext not in supported_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload a PDF, TXT, or DOCX file.",
        )

    contents = await file.read()

    file_path = ""

    # Save PDFs because the PDF processing pipeline
    # uses the uploaded file path.
    if file_ext == "pdf":
        file_path = f"./temp_{file.filename}"

        with open(file_path, "wb") as f:
            f.write(contents)

        print("Sales PDF saved:", file_path)

    human_message = HumanMessage(
        content=f"User uploaded sales document: {file.filename}"
    )

    global_state["messages"] = [human_message]
    global_state["file_type"] = file_ext
    global_state["contents"] = contents
    global_state["file_path"] = file_path

    graph = build_graph()

    result = graph.invoke(global_state)

    print("From AI Message:")
    print(result.get("messages"))

    ai_message = result["messages"][-1]

    try:
        final_result = json.loads(ai_message.content)
    except json.JSONDecodeError:
        final_result = {
            "message": ai_message.content
        }

    print("Final result:", final_result)

    return JSONResponse(
        content=final_result,
        status_code=200,
    )


@app.get("/")
def root():
    return {
        "message": "Sales Document Reader API is running"
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
