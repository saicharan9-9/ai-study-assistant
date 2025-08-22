from pydantic import BaseModel

class QuizRequest(BaseModel):
    text: str
    language: str

class QARequest(BaseModel):
    question: str
    context: str
    language: str

class ProgressUpdate(BaseModel):
    user: str
    subject: str
    chapter: str
    score: int
