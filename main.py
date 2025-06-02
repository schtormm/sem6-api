import codecs
import csv
import json
import os
import random

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from openai import AzureOpenAI

from customTypes import AnswerRequest, ChatRequest
from utils import convertRecommendationToModel

load_dotenv()
# LLM settings
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")

if not endpoint or not deployment or not api_key:
    raise ValueError("Please set the AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, and AZURE_OPENAI_API_KEY environment variables.")

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
                #pick three random recommendations from the filtered data
                if len(data) > 3:
                    random_recommendations = random.sample(data, 3)
                else:
                    random_recommendations = data
                #convert to Recommendation model
                if not random_recommendations:
                    raise HTTPException(status_code=404, detail="No recommendations found with the given rating")
                converted_recommendations = []
                for recommendation in random_recommendations:
                    converted_recommendations.append(convertRecommendationToModel(recommendation))
    

    except csv.Error as e:
            raise HTTPException(status_code=500, detail="File is empty or corrupted")
        
    return {"recommendation": converted_recommendations}

@app.post("/recommendations")
def parse_answers(request: AnswerRequest):
    try:
        return {
            "client": request.client,
            "recommendations": get_locations()["recommendation"]
        }
    
    except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format")


client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=api_key,
)

with open("System_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

@app.post("/chat")
async def chat(request: ChatRequest):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.user_prompt},
        ],
        max_tokens=1024,
        temperature=0.5,
        model=deployment,
    )
    return {"response": response.choices[0].message.content}