import json
import pandas
import pickle
import pandas as pd
import os
import tweepy as tw


class Tweet():
    '''
    Class to extract relevant information from each tweets
    Args: @Input: Tweepy object called status
          @Output: dictionary with the relevant information (see method _tweet_page of class User)
    '''
    def __init__(self,status):
        self.date = status.created_at
        self.username = status.user.screen_name
        self.user_id = status.user.id
        self.tweet_id = status.id
        self.text = status.full_text
        self.hashtags = status.entities['hashtags']
        self.user_mentions = status.entities['user_mentions']
        self.replying_to_tweet = status.in_reply_to_status_id
        self.replying_to_user_id = status.in_reply_to_user_id
        self.retweeted = status.retweeted

    def tweet_row(self):
        return {'date': self.date,'username': self.username,
        'user_id':self.user_id,'tweet_id':self.tweet_id,
        'text':self.text,'hashtags':self.hashtags,'user_mentions':self.user_mentions,
        'replying_to_tweet':self.replying_to_tweet,'replying_to_user_id':self.replying_to_user_id,'retweeted':self.retweeted}

class User():

    '''
    Each user has in own class to manage its personal information and the
    tweets retrieval
    Args:
        - username: current username under study
        - tweets: pandas dataframe with the relevant infortmation
        - page where we are currently getting the TWEETS
        - warnings: in order to stop scraping this user we need to know when twitter stops providing tweets of this user

    '''

    def __init__(self, username):
        self.username = username
        self.tweets = pd.DataFrame(columns=['date','username','user_id','tweet_id','text','hashtags','user_mentions','replying_to_tweet','replying_to_user_id','retweeted'])
        self.page = 0
        self.warnings = 0

    def get_all_tweets(self,api):

        '''
        Inspect all the pages until pages are empty retrieving all the tweets
        '''

        file_tweets = './Users_tweets/' + self.username + '.csv'
        if not os.path.isfile(file_tweets):
            while self.warnings < 2:
                cur_list_status = api.user_timeline(screen_name = self.username,
                              result_type = 'recent', tweet_mode='extended',
                              count = 200,page=self.page)

                if len(cur_list_status) != 0:
                    self._tweet_page(cur_list_status)
                else:
                    self.warnings += 1

    def _tweet_page(self,cur_list_status):
        for status in cur_list_status:
            tweet = Tweet(status)
            self.tweets = self.tweets.append(tweet.tweet_row(),ignore_index=True)
        self.page += 1

    def _read_element(element):
        status = element
        json_str = json.dumps(status._json)
        parsed = json.loads(json_str)
        return parsed

    def save_csv(self):
        file = './Users_tweets/' + self.username + '.csv'
        self.tweets.to_csv(file)

    @classmethod
    def user_initialization(cls,username,basic_info_user):
        # saving users infortmation
        file = './Users_info/' + username + '.pickle'
        if not os.path.isfile(file):
            with open(file, 'wb') as handle:
                pickle.dump(basic_info_user,handle,protocol=pickle.HIGHEST_PROTOCOL)

        return cls(username)
