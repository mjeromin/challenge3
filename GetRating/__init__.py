import logging

import azure.functions as func


#GetRating
#Verb: GET
#Query string or route parameter: ratingId
#Requirements
#Get the rating from your database and return the entire JSON payload for the review identified by the id
#Additional route parameters or query string values may be used if necessary.
#Output payload example:
#{
#  "id": "79c2779e-dd2e-43e8-803d-ecbebed8972c",
#  "userId": "cc20a6fb-a91f-4192-874d-132493685376",
#  "productId": "4c25613a-a3c2-4ef3-8e02-9c335eb23204",
#  "timestamp": "2018-05-21 21:27:47Z",
#  "locationName": "Sample ice cream shop",
#  "rating": 5,
#  "userNotes": "I love the subtle notes of orange in this ice cream!"
#}

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
        my_id =  items[0]['id']
        my_userId = items[0]['userId']
        my_productId = items[0]['productId']
        my_timestamp = items[0]['timestamp']
        my_locationName = items[0]['locationName']
        my_rating = items[0]['rating']
        my_userNotes = items[0]['userNotes']
        output_payload ='{{\n\t"id": "{}"\n\t"userId": "{}"\n\t"productId": "{}"\n\t"timestamp": "{}"\n\t"locationName": "{}"\n\t"rating": "{}"\n\t"userNotes": "{}"\n}}'.format(my_id,
                                                                                                                                                                      my_userId,
                                                                                                                                                                      my_productId,\
                                                                                                                                                                          my_timestamp,
                                                                                                                                                                          my_locationName,
                                                                                                                                                                          my_rating,
                                                                                                                                                                          my_userNotes)
        return func.HttpResponse(output_payload)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=405
        )