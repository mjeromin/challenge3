import logging
import json
import azure.functions as func

def main(req: func.HttpRequest, items: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not items:
        logging.warning("Ratings item not found")
    else:
        logging.info("Found ratings item, ID=%s",
                     items[0]['id'])

    if 'ratingId' in list(req.params):
        ratingId = req.params.get('ratingId')
    else:
        ratingId = None
    if not ratingId:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse("Incorrect usage, must supply ratingId, status 406", status_code=406)
        else:
            ratingId = req_body.get('ratingId')

    if ratingId and not items:
        return func.HttpResponse("Rating not found, status 404", status_code=404)
    elif ratingId:
        return func.HttpResponse(json.dumps(ratingId))
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=405
        )