import codecs
import csv
import json
import random

from fastapi import FastAPI, File, HTTPException, Request, UploadFile

from customTypes import AnswerRequest
from utils import convertRecommendationToModel

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello world!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/locations")
def get_locations(minimum_rating: float = 0.0):
    if minimum_rating < 0 or minimum_rating > 5:
        raise HTTPException(status_code=400, detail="Minimum rating must be between 0 and 5")
    try:
        with open('fakedata.csv', 'r') as file:
                csvreader = csv.DictReader(file)  

                data = list(csvreader)
                if not data:
                    raise HTTPException(status_code=500, detail="File is empty or corrupted")
                #filter out recommendations with a rating lower than the minimum rating
                if minimum_rating > 0 and minimum_rating <= 5:
                    data = [row for row in data if float(row["Beoordeling"]) >= minimum_rating]
                #pick random recommendation
                random_recommendation = random.choice(data)
                #convert to dictionary
                random_recommendation = dict(random_recommendation)

    except csv.Error as e:
            raise HTTPException(status_code=500, detail="File is empty or corrupted")
        
    return {"recommendation": convertRecommendationToModel(random_recommendation)}

@app.get("/recommendations")
async def parse_answers(request: AnswerRequest):
    try:
        return {
            "client_id": request.client,
            "parsed_answers": [answer.model_dump() for answer in request.answers]
        }
    except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while processing the request")
