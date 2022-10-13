import logging
import datetime
import uuid
import json
import requests

import azure.functions as func

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.') 
    request_body = req.get_json()

    request_body['id'] = str(uuid.uuid4())
    request_body['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%SZ")
    if request_body['rating'] < 0 or request_body['rating'] > 5:
        return func.HttpResponse('INVALID rating, MUST BE between 0-5', status_code=405)
    r = requests.get('https://serverlessohapi.azurewebsites.net/api/GetUser?userId='+request_body['userId'])
    if r.status_code != 200:
        return func.HttpResponse('INVALID userID, must already exist.', status_code=407)
    r = requests.get('https://serverlessohapi.azurewebsites.net/api/GetProduct?productId='+request_body['productId'])
    if r.status_code != 200:
        return func.HttpResponse('INVALID productID, must already exist.', status_code=408)

    # check everything before writing
    doc.set(func.Document.from_json(json.dumps(request_body)))

    return func.HttpResponse(json.dumps(request_body))