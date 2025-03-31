import codecs
import csv
import random

from fastapi import FastAPI, File, UploadFile

from utils import convertRecommendationToModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello world!"}

@app.post("/submit-results")
def read_csv(file: UploadFile = File(...)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    data = {}
    for rows in csvReader:
        key = rows["test"]
        data[key] = rows
        
    file.file.close()
    # ADS&AI black magic goes here
    return {"data": data}

@app.get("/health")
def health():
        return {"status": "ok"}

@app.get("/recommendation")
def recommendation(minimum_rating: float = 0.0):
    with open('AI data(Sheet1).csv', 'r') as file:
        csvreader = csv.DictReader(file)

        data = list(csvreader)
        #filter out recommendations with a rating lower than the minimum rating
        data = [row for row in data if float(row["Beoordeling"]) >= minimum_rating]
        #pick random recommendation
        random_recommendation = random.choice(data)
        #convert to dictionary
        random_recommendation = dict(random_recommendation)

        return {"recommendation": convertRecommendationToModel(random_recommendation)}
    
