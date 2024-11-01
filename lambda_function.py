import json

def handler(event, context):
    '''
    handler
    '''
    name = event.get("name", "John Doe")

    return json.dumps( {"statusCode": 200, "message": f"Hello {name}! Welcome!"})
