import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, items: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not items:
        logging.warning("Ratings item not found")
    else:
        for item in items:
            logging.info("Found ratings item, ID=%s",
                     item['id'])

    if 'userId' in list(req.params):
        userId = req.params.get('userId')
    else:
        userId = None
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Incorrect usage, must supply userId, status 406", status_code=406)
        else:
            userId = req_body.get('userId')

    if userId and not items:
        return func.HttpResponse("User ratings not found, status 404", status_code=404)
    elif userId:
        my_items = []
        for item in items:
            my_item = {}
            my_item['id'] = item['id']
            my_item['userId'] = item['userId']
            my_item['productId'] = item['productId']
            my_item['timestamp'] = item['timestamp']
            my_item['locationName'] = item['locationName']
            my_item['rating'] = item['rating']
            my_item['userNotes'] = item['userNotes']
            my_items.append(my_item)
        return func.HttpResponse(json.dumps(my_items))
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=405
        )