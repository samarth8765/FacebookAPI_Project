# Import external modules
import facebook
import requests
# Import internal modules
from config import TOKEN, APP_ID, APP_SECRET


def get_graph(token: str=TOKEN, app_id: str=APP_ID,
              app_secret: str=APP_SECRET) -> tuple:
    """
    This function use the USER ACCESS TOKEN to connect to the GraphApi.
    Then, it extends the token so that it lasts more than 15 minutes. This
    is done following:
    https://stackoverflow.com/questions/26594829/how-to-extend-my-facebook-graph-api-token-in-python

    :param token: USER ACCESS TOKEN
    :type token: str
    :param app_id: APP_ID
    :type app_id: str
    :param app_secret: APP_SECRET
    :type app_secret: str
    :return: graph, extended_token
    :rtype tuple
    """
    graph = facebook.GraphAPI(token)
    extended_token = graph.extend_access_token(app_id, app_secret)
    return graph, extended_token


def get_fb_token(app_id: str=APP_ID, app_secret: str=APP_SECRET) -> str:
    """
    This function takes in an app_id and an app_secret and returns an access
    token. (Not an user access token!)
    Where to find app_id and app_secret?
    Go to: https://developers.facebook.com/
    then go to MyApps and click on your app, then settings, basics.

    :param app_id: APP_ID
    :type app_id: str
    :param app_secret: APP_SECRET
    :type app_secret: str
    :return: access token
    :rtype: str
    """
    url = 'https://graph.facebook.com/oauth/access_token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret,
        'redirect_uri': 'https://www.facebook.com/connect/login_success.html'
    }
    response = requests.post(url, params=payload)
    return response.json()['access_token']


if __name__ == "__main__":
    # Get token
    print("Original Token: ", TOKEN)
    t = get_fb_token()
    print("Token with get_fb_token: ", t)
    g, ext_token = get_graph()
    print("Token with get_graph(): ", ext_token)
