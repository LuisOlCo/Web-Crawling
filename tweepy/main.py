import os
import tweepy as tw
import pandas as pd
import json
import pickle
from user_class import User
import time

def auth_api():
    Twitter_login=pickle.load(open('secret_twitter_credentials.pkl','rb'))
    auth = tw.OAuthHandler(Twitter_login['Consumer Key'], Twitter_login['Consumer Secret'])
    auth.set_access_token(Twitter_login['Access Token'], Twitter_login['Access Token Secret'])
    api = tw.API(auth, wait_on_rate_limit=True)
    return api

def read_element(element):
    status = element
    json_str = json.dumps(status._json)
    parsed = json.loads(json_str)
    return parsed

def main():
    # Authentification
    api = auth_api()

    users = pd.read_csv('depressed_username_and_userid.csv')['username'].tolist()

    for username in users:
        print('USERNAME: ',username)
        try:
            basic_info_user = api.get_user(screen_name = username)
            # get basic information from the user
            cur_user = User.user_initialization(username,basic_info_user)
            #print(cur_user.username)
            #print(cur_user.tweets)
            #print(cur_user.page)
            cur_user.get_all_tweets(api)
            cur_user.save_csv()
            print(cur_user.username)
            print(cur_user.tweets)
            print(cur_user.page)

            print('KILL PROCRESS NOW')
            time.sleep(5)
        except tw.TweepError as error:
            print(error)


if __name__ == '__main__':
    main()
