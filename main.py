import codecs
import csv
import json
import random

from fastapi import FastAPI, File, HTTPException, Request, UploadFile

from utils import convertRecommendationToModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello world!"}

@app.post("/submit-results")
def read_csv(file: UploadFile = File(...)):
    try:
        # Check if the file is a CSV
        if not file.filename.endswith('.csv'):
            return {"error": "File is not a CSV"}
        csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
        #check if CSV is empty or corrupted
        if csvReader is None:
            return {"error": "File is empty or corrupted"}
        data = {}
        for rows in csvReader:
            key = rows["test"]
            data[key] = rows
        
        file.file.close()
        return {"data": data}
    # ADS&AI black magic goes here
    except csv.Error as e:
        return {"error": "File is empty or corrupted"}
    except Exception as e:
        return {"error": "An error occurred while processing the file"}
    

@app.get("/health")
def health():
        return {"status": "ok"}

@app.get("/recommendation")
def recommendation(minimum_rating: float = 0.0):
    with open('AI data(Sheet1).csv', 'r') as file:
        csvreader = csv.DictReader(file)

        data = list(csvreader)
        #filter out recommendations with a rating lower than the minimum rating
        if minimum_rating > 0 and minimum_rating <= 5:
            data = [row for row in data if float(row["Beoordeling"]) >= minimum_rating]
        #pick random recommendation
        random_recommendation = random.choice(data)
        #convert to dictionary
        random_recommendation = dict(random_recommendation)

        return {"recommendation": convertRecommendationToModel(random_recommendation)}
    
@app.post("/unity-results")
async def get_results(request: Request):
        try:
            #get body from request
            body =  await request.json()
            #get the data from the body
            data = body["test"]
            #convert to dictionary
            data = dict(data)
            print(data)
            return {"test": 100, "data": data}
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        except Exception as e:
            raise HTTPException(status_code=500, detail="An error occurred while processing the request")