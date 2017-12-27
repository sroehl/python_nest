import http.client
from urllib.parse import urlparse
import json
import sys
import boto3


def read_config():
    client_id = ''
    client_secret = ''
    auth_code = ''
    try:
        with open('config.cfg', 'r') as config_file:
            for line in config_file:
                key, value = line.split(':')
                if key == 'CLIENT_ID':
                    client_id = value
                elif key == 'CLIENT_SECRET':
                    client_secret = value
                elif key == 'AUTH_CODE':
                    auth_code = value
    except FileNotFoundError as ex:
        print('config.cfg file was not found containing client_id, client_secret, and auth_code: {}'.format(ex))
    if client_id == '' or client_secret == '' or auth_code == '':
        print('client_id, client_secret, and/or auth_code not correctly set in file.\nExiting...')
        sys.exit(-1)
    return client_id, client_secret, auth_code

def read_config_from_dynamo(id):
    client_id = ''
    client_secret = ''
    auth_code = ''
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('HomeTempConfig')
        result = table.get_item(TableName='HomeTempConfig', Key={'id':id})
        if 'Item' in result:
            client_id = result['Item']['client_id']
            client_secret = result['Item']['client_secret']
            auth_code = result['Item']['auth_code']
    except Exception as ex:
        print('Could not find record containing client_id, client_secret, and auth_code: {}'.format(ex))
    if client_id == '' or client_secret == '' or auth_code == '':
        print('client_id, client_secret, and/or auth_code not correctly set.\nExiting...')
        sys.exit(-1)
    return client_id, client_secret, auth_code


def get_token_from_nest(client_id, client_secret, auth_code, is_lambda=False):
    conn = http.client.HTTPSConnection("api.home.nest.com")
    payload = "code={}&client_id={}&client_secret={}&grant_type=authorization_code".format(auth_code, client_id,
                                                                                           client_secret)
    headers = {'content-type': "application/x-www-form-urlencoded"}
    conn.request("POST", "/oauth2/access_token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token_data = json.loads(data.decode("utf-8"))
    print(token_data)
    if 'access_token' in token_data:
        token = token_data['access_token']
        if not is_lambda:
            write_token_to_file(token)
        return token
    return None


def write_token_to_file(token):
    with open('token.data', 'w') as token_file:
        token_file.write(token)


def read_token_from_file():
    try:
        with open('token.data', 'r') as token_file:
            token = token_file.read()
        return token
    except FileNotFoundError:
        return None


def get_token():
    token = read_token_from_file()
    if token is None:
        read_config()
        try:
            client_id, client_secret, auth_code = read_config()
            token = get_token_from_nest(client_id, client_secret, auth_code)
        except Exception as ex:
            print("Unable to get token from Nest: {}".format(ex))
    return token

def get_token_lambda(id):
    client_id, client_secret, auth_code = read_config_from_dynamo(id)
    token = get_token_from_nest(client_id, client_secret, auth_code, is_lambda=True)
    return token

def get_token_from_dynamo(id):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('HomeTempConfig')
        result = table.get_item(TableName='HomeTempConfig', Key={'id':id})
        if 'Item' in result:
            return result['Item']['token']
    except Exception as ex:
        print("Could not find record for id {}".format(id))
    return None



def read_data(token):
    conn = http.client.HTTPSConnection("developer-api.nest.com")
    headers = {'authorization': "Bearer {0}".format(token)}
    conn.request("GET", "/", headers=headers)
    response = conn.getresponse()

    if response.status == 307:
        redirectLocation = urlparse(response.getheader("location"))
        conn = http.client.HTTPSConnection(redirectLocation.netloc)
        conn.request("GET", "/", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            raise Exception("Redirect with non 200 response")

    data = response.read()
    # print(data.decode("utf-8"))
    return json.loads(data.decode("utf-8"))


def get_weather_data(zipcode):
    apikey = '9852a963bac2a8b12d047b07ec7e20bb'
    conn = http.client.HTTPConnection("api.openweathermap.org")
    conn.request("GET", "/data/2.5/weather?zip={},us&units=imperial&appid={}".format(zipcode, apikey))
    response = conn.getresponse()

    data = response.read()
    return json.loads(data.decode("utf-8"))

if __name__ == '__main__':
    nest_token = get_token()
    nest_data = read_data(nest_token)
    print(nest_data['devices']['thermostats'])
