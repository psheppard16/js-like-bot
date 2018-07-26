__author__ = 'Preston Sheppard'
from imgurpython import ImgurClient
import requests
import pickle
from pprint import pprint

def getAuthClient(clientId, clientSecret):
    client = ImgurClient(clientId, clientSecret)
    refreshToken = loadRefreshToken()
    if not refreshToken:
        authorization_url = client.get_auth_url('pin')
        print(authorization_url)
        pin = input("Enter the pin given by the link:")
        credentials = client.authorize(pin, 'pin')
        saveRefreshToken(credentials['refresh_token'])
        client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
        return client, credentials['access_token'], credentials['refresh_token']
    else:
        refreshToken = loadRefreshToken()
        accessToken = getAccessToken(clientId, clientSecret, refreshToken)
        client.set_user_auth(accessToken, refreshToken)
        return client, accessToken, refreshToken

def getAccessToken(clientId, clientSecret, refreshToken):
    endPoint = "https://api.imgur.com/oauth2/token"

    data = {'refresh_token': refreshToken,
            'client_id': clientId,
            'client_secret': clientSecret,
            'grant_type': "refresh_token"}

    request = requests.post(endPoint, data=data)
    accessToken = request.json()['access_token']
    return accessToken

def uploadImage(accessToken):
    endPoint = "https://api.imgur.com/3/image"

    imageData = {'description': "Test description",
            'name': 'Test Name',
            'title': "Test Title",
            'image': open('Testing.jpg', 'rb').read(),
            'type': "image/jpeg"}

    headers = {'Authorization': 'Bearer ' + accessToken}

    request = requests.post(endPoint, data=imageData, headers=headers)
    r = request.json()
    return r['data']['id'], r['data']['title']

def shareImage(accessToken, imageId, imageTitle):
    endPoint = "https://api.imgur.com/3/gallery/image/" + imageId

    headers = {'Authorization': 'Bearer ' + accessToken}

    postData = {'title': imageTitle}

    request = requests.post(endPoint, data=postData, headers=headers)

    pprint(request.json())

def loadRefreshToken():
    filePath = "refreshToken.txt"
    try:
        with open(filePath, 'rb') as input:
            return pickle.load(input)
    except EOFError and FileNotFoundError:
        raise Exception("File not found")

def saveRefreshToken(refreshToken):
    filePath = "refreshToken.txt"
    try:
        with open(filePath, 'wb') as output:
            pickle.dump(refreshToken, output, pickle.HIGHEST_PROTOCOL)
    except EOFError and FileNotFoundError:
        raise Exception("File not found")

clientId = "1a73509dbf251cf"
clientSecret = "3cc02c2a34878b0ce3cd9d81820dc514b34b0f34"
imgurClient, accessToken, refreshToken = getAuthClient(clientId, clientSecret)
imageId, imageTitle = uploadImage(accessToken)
shareImage(accessToken, imageId, imageTitle)