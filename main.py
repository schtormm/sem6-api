import codecs
import csv
import random

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

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
def recommendation():
    with open('AI data(Sheet1).csv', 'r') as file:
        csvreader = csv.reader(file)
        # Skip header row if it exists
        next(csvreader)
        # Convert to list to get random choice
        data = list(csvreader)
        random_row = random.choice(data)
        return {"recommendation": random_row}
    