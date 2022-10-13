import logging

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
        item_count = len(items)
        output_payload = '['
        for i, item in enumerate(items):
            my_id =  item['id']
            my_userId = item['userId']
            my_productId = item['productId']
            my_timestamp = item['timestamp']
            my_locationName = item['locationName']
            my_rating = item['rating']
            my_userNotes = item['userNotes']
            output_payload +='\n\t{{\n\t"id": "{}"\n\t"userId": "{}"\n\t"productId": "{}"\n\t"timestamp": "{}"\n\t"locationName": "{}"\n\t"rating": "{}"\n\t"userNotes": "{}"\n'.format(my_id,
                                                                                                                                                                      my_userId,
                                                                                                                                                                      my_productId,\
                                                                                                                                                                          my_timestamp,
                                                                                                                                                                          my_locationName,
                                                                                                                                                                          my_rating,
                                                                                                                                                                          my_userNotes)
            if i < item_count:
                output_payload += '\t},\n'
            else:
                output_payload += '\t}\n'
        output_payload += ']'
        return func.HttpResponse(output_payload)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=405
        )