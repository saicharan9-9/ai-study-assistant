import os
import tempfile
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from googletrans import Translator

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizRequest(BaseModel):
    text: str
    language: str

class QARequest(BaseModel):
    question: str
    context: str
    language: str

translator = Translator()

def extract_text_from_pdf(pdf_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        reader = PdfReader(tmp.name)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

def ocr_image(file_bytes):
    image = Image.open(tempfile.NamedTemporaryFile(delete=False, suffix=".png"))
    image.save(image.filename)
    text = pytesseract.image_to_string(Image.open(image.filename))
    return text

def summarize(text, language="en"):
    prompt = f"Summarize the following in simple points:\n\n{text}\n"
    # Use OpenAI API or HuggingFace model here
    llm = OpenAI(temperature=0.3)
    summary = llm(prompt)
    if language != "en":
        summary = translator.translate(summary, dest=language).text
    return summary

def generate_flashcards(text, language="en"):
    prompt = f"Create 10 flashcards (question:..., answer:...) from this material:\n\n{text}\n"
    llm = OpenAI(temperature=0.3)
    flashcards = llm(prompt)
    if language != "en":
        flashcards = translator.translate(flashcards, dest=language).text
    return flashcards

def generate_mcqs(text, language="en"):
    prompt = f"Create 10 MCQs with 4 options each (mark correct answer) from:\n{text}\n"
    llm = OpenAI(temperature=0.3)
    mcqs = llm(prompt)
    if language != "en":
        mcqs = translator.translate(mcqs, dest=language).text
    return mcqs

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
        text = ocr_image(content)
    else:
        text = content.decode("utf-8")
    return {"text": text}

@app.post("/summarize")
async def summarize_endpoint(req: QuizRequest):
    summary = summarize(req.text, req.language)
    return {"summary": summary}

@app.post("/flashcards")
async def flashcards_endpoint(req: QuizRequest):
    cards = generate_flashcards(req.text, req.language)
    return {"flashcards": cards}

@app.post("/mcqs")
async def mcqs_endpoint(req: QuizRequest):
    mcqs = generate_mcqs(req.text, req.language)
    return {"mcqs": mcqs}

@app.post("/rag_qa")
async def rag_qa(req: QARequest):
    # Use RAG: retrieve relevant chunk, then generate answer
    # For MVP: just use context+question in LLM
    prompt = f"Using only this material:\n{req.context}\nAnswer: {req.question}\n"
    llm = OpenAI(temperature=0.2)
    answer = llm(prompt)
    if req.language != "en":
        answer = translator.translate(answer, dest=req.language).text
    return {"answer": answer}

# Add endpoints for dashboard, progress tracking, etc as needed
