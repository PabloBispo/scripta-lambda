def handler(event, context):
    '''
    handler
    '''
    name = event.get("name", "John Doe")

    return {"statusCode": 200, "message": f"Hello {name}! Welcome!"}
