import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table('MyTable')


class PythonObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,
                      (list, dict, str, unicode,
                       int, float, bool, type(None))):
            return json.JSONEncoder.default(self, obj)
        elif hasattr(obj, '__repr__'):
            return obj.__repr__()
        else:
            return json.JSONEncoder.default(self, obj.__repr__())

def result(event, context):
    response = table.scan(ConsistentRead=True)
    stat = writeResultstos3(response['Items'])
    return stat

def writeResultstos3(result):
        strg=json.dumps(result,cls=PythonObjectEncoder)
        strg=strg.replace('Decimal(','')
        val=strg.replace(')','')
        print val
        s3.put_object(Bucket='vote.itrends.online',Key='data.json',Body=val)
        return val
