from datetime import time
from typing import List, Literal

from pydantic import BaseModel


class OpeningHours (BaseModel):
    open: time
    close: time

class Recommendation(BaseModel):
     category: str
     name: str
     priceClass : Literal["goedkoop", "midden", "duur", ""]
     kitchen: str
     concept: str
     atmosphere: str
     style: str
     location: str
     openingHours: OpeningHours
     rating: float

class Answer(BaseModel):
    id: str
    question_type: str
    answer: str

class AnswerRequest(BaseModel):
    client: str
    answers: List[Answer]
