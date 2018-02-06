from __future__ import print_function

import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')
try:
    db = boto3.resource('dynamodb').Table('MyTable')
except:
    print("issue in db con")
def todb(event, context):
    #print(event['body']['Name'])
    try:
        if event['body']['Name']:
            response = db.update_item(Key={ "Name": event['body']['Name']}, 
              UpdateExpression='SET #oldVote = #oldVote + :newVote', 
              ExpressionAttributeNames={ '#oldVote' :'Vote'}, 
              ExpressionAttributeValues={':newVote': 1} 
              )
            #print(response)
        return "voted"
    except:
        return event

