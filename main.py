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

# @app.post("/submit-results")
# def read_csv(file: UploadFile = File(...)):
#     try:
#         # Check if the file is a CSV
#         if not file.filename.endswith('.csv'):
#             return {"error": "File is not a CSV"}
#         csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
#         #check if CSV is empty or corrupted
#         if csvReader is None:
#             return {"error": "File is empty or corrupted"}
#         data = {}
#         for rows in csvReader:
#             key = rows["test"]
#             data[key] = rows
        
#         file.file.close()
#         return {"data": data}
#     # ADS&AI black magic goes here
#     except csv.Error as e:
#         return {"error": "File is empty or corrupted"}
#     except Exception as e:
#         return {"error": "An error occurred while processing the file"}
    

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
                 "parsed_answers": [answer.model_dump for answer in request.answers]
            }
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while processing the request")

    # #get body from request
    #         body =  await request.json()
    #         #check if body is empty or corrupted
    #         if not body:
    #             raise HTTPException(status_code=400, detail="Body is empty or corrupted")
    #         #check if body is a dictionary
    #         if not isinstance(body, dict):
    #             raise HTTPException(status_code=400, detail="Body is not a dictionary")
    #         #get the data from the body
    #         data = body["answers"]
    #         # if data is not there, raise an error
    #         if not data:
    #             raise HTTPException(status_code=400, detail="Data is empty or corrupted")
    #         # ensure data is a list, no need to convert to dict
    #         if not isinstance(data, list):
    #             raise HTTPException(status_code=400, detail="Answers must be a list")
    #         # get the client id
    #         client_id = body.get("client")
    #         if not client_id:
    #             raise HTTPException(status_code=400, detail="Client ID is missing")
    #         # check if client_id is a valid UUID
    #         if not isinstance(client_id, str):
    #             raise HTTPException(status_code=400, detail="Client ID must be a string")
    #         # parse the answers
    #         parsed_answers = []
    #         for answer in data:
    #             if not isinstance(answer, dict):
    #                 raise HTTPException(status_code=400, detail="Answer must be a dictionary")
    #             answer_id = answer.get("id")
    #             question_type = answer.get("question_type")
    #             answer_value = answer.get("answer")
    #             if not answer_id or not question_type or answer_value is None:
    #                 raise HTTPException(status_code=400, detail="Answer is missing required fields")
    #             parsed_answers.append({
    #                 "id": answer_id,
    #                 "question_type": question_type,
    #                 "answer": answer_value
    #             })
    #         return (f"Client ID: {client_id}, Parsed Answers: {parsed_answers}")