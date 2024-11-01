def handler(event, context):
    '''
    handler
    '''
    name = event["name"]

    return {"statusCode": 200, "message": f"Hello {name}! Welcome!"}
