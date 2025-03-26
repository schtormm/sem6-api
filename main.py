import codecs
import csv

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def read_csv(file: UploadFile = File(...)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    data = {}
    for rows in csvReader:
        key = rows["test"]
        data[key] = rows
        
    file.file.close()
    print(data)
    return {"status": "ok", "data": data, "message": "Hello World"}
