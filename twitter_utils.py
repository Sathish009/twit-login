import oauth2
import constants
import urlparse as urlparse

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

def getRequestToken():
    client = oauth2.Client(consumer)
    # use the client to perform a request for request token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
    if response.status !=200:
        print('An error has occurred getting the request token')

    #get the request token parsing the query str returned
    return dict(urlparse.parse_qsl(content.decode('utf-8')))

def getOauthVerifier(request_token):
    # ask the user to authorize the app and give us the PIN
    print("Goto following url")
    print(getOauthVerifierUrl(request_token))

    return input("what is the PIN?")

def getOauthVerifierUrl(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token'])

def getAccessToken(request_token,oauth_verifier):
    # create a request token which containts the request token and verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # create a client with our consumer and newly created (verified) token
    client = oauth2.Client(consumer, token)

    # ask twitter for access token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return dict(urlparse.parse_qsl(content.decode('utf-8')))
