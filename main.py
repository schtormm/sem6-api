import codecs
import csv

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