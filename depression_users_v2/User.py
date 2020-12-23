import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class Tweet():
    '''
    Extract froms selenium tweet objects the information needed, so it can be
    added to the csv file with the rest of the user's tweets
    '''
    def __init__(self,tweet):
        '''
        Initializate all the css tags of interest.
        '''
        self.tweet = tweet
        self.css_username = 'div.css-901oao.css-bfa6kz.r-18jsvk2.r-1qd0xha.r-a023e6.r-b88u0q.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
                     # 'div.css-901oao.css-bfa6kz.r-hkyrab.r-1qd0xha.r-a023e6.r-b88u0q.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
        self.css_user_tag = 'div.css-901oao.css-bfa6kz.r-m0bqgq.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
                     # 'div.css-901oao.css-bfa6kz.r-1re7ezh.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
        self.css_tweet = 'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'
                  # 'div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'
        self.css_date =  'div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2'
                  # 'a.css-4rbku5.css-18t94o4.css-901oao.r-m0bqgq.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
                  # 'a.r-1re7ezh.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0.css-4rbku5.css-18t94o4.css-901oao'
        self.css_retweet = 'a.css-4rbku5.css-18t94o4.css-901oao.r-m0bqgq.r-1loqt21.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
                    # 'a.css-4rbku5.css-18t94o4.css-901oao.r-1re7ezh.r-1loqt21.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
    def descomposing_tweet(self,driver):

        '''
        Decompose the selenium web element into the elements of interest, return a dictionary to
        to the pandas variable along the rest of the tweets of the user
        '''
        #USERNAME
        self._waiting_func(driver,self.css_username)
        username = self.tweet.find_element_by_css_selector(self.css_username).text

        #USER_TAG
        self._waiting_func(driver,self.css_user_tag)
        user_tag = self.tweet.find_element_by_css_selector(self.css_user_tag).text

        # TEXT
        try:
            self._waiting_func(driver,self.css_tweet)
            text = self.tweet.find_element_by_css_selector(self.css_tweet).text
        except:
            text = 'No text'

        #DATE
        self._waiting_func(driver,self.css_date)
        date_ob = tweet.find_element_by_css_selector(self.css_date)
        ad = date_ob.find_elements_by_tag_name("time")
        #attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', ad[0])
        last_date = datetime.datetime.strptime(ad[0].get_attribute('datetime'), "%Y-%m-%dT%H:%M:%S.000Z")


        # Replies, Retweets & Likes
        self._waiting_func(driver,"div[data-testid='reply']")
        replies = self.tweet.find_element_by_css_selector("div[data-testid='reply']").text
        retweets = self.tweet.find_element_by_css_selector("div[data-testid='retweet']").text
        likes = self.tweet.find_element_by_css_selector("div[data-testid='like']").text

        # Retweet?
        # Needs to be reviewed
        self._waiting_func(driver,self.css_retweet)
        try:
            if 'Retweeted' in tweet.find_element_by_css_selector(self.css_retweet).text:
                retweet = True
            else:
                retweet = False
        except:
            retweet = False

        # New row for the pandas with all the info of the current tweet
        tweet_row = {'Username':username,'User_tag':user_tag,'Date':last_date,'Tweet':text,'Replies':replies,'Retweets':retweets,'Likes':likes,'Retweet':retweet}
        return tweet_row

    def _waiting_func(self,driver,my_element_id):
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        try: #$find_element_by_class_name
            WebDriverWait(driver, 4,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, my_element_id)))
        except : #(NoSuchElementException, TimeoutException)
            print('Loading took too much time, may be not results')


class User():
    '''
    Class to track all the tweets of the user given the period of time
    '''
    def __init__(self,joined_date,user_tag):
        # time variables
        self.joined_date = joined_date
        self.finish_time  = date(2020,11,13)
        self.proposed_start_time = date(2019,10,1)
        # self.start_time is a dynamic variable that will constanly change
        self.start_time = _find_start_time()

        self.user_tag = user_tag
        self.status = status
        self.tweets = pd.DataFrame(columns=['Username','User_tag','Date','Tweet','Replies','Retweets','Likes','Retweet'])

    def get_timeframe_for_crawling(self):
        end_time = self.start_time + timedelta(days=5)
        start_time_str = str(self.start_time.year) + '-' + str(self.start_time.month) + '-' + str(self.start_time.day)
        end_time_str = str(end_time.year) + '-' + str(end_time.month) + '-' + str(end_time.day)
        print('Period: ' + start_time_str + ' / ' + end_time_str)
        # at the end of the iteration end_time has to be the new self.start_time
        return start_time_str,end_time_str,end_time

    def retrieving_tweets_from_user(self,driver,end_time):
        '''
        Given a timeframe and an username, this method find all the tweet this users
        made during the period of time given. It scrolls down the page until it has
        collected all the tweets
        '''

        times = 0
        previous_location = None
        red_flag = 0
        done = False
        last_location = 0
        while True:
            print('**********************')
            print('Number of time it has scrolled down: ',times)
            print('**********************')
            times += 1
            # Check if there are tweets for this period of time
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$
            # CREATE A METHOD TO CHECK RIGHT AWAY IF THERE IS ANY TWEET IN THIS PERIOD OF TIME
            # $$$$$$$$$$$$$$$$$$$$$$$$$$$$
            init_height = driver.execute_script("return document.body.scrollHeight")
            time.sleep(0.2)

            # 'div.css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll.r-1ny4l3l'
            css_tweets = 'div.css-1dbjc4n.r-j7yic.r-qklmqi.r-1adg3ll.r-1ny4l3l'
            self._waiting_func(driver,css_tweets)
            tweets = driver.find_elements_by_css_selector(css_tweets)

            print('Number of tweets found: ',len(tweets))
            if len(tweets) > 0:
                for i in range(len(tweets)):
                    # checking each of the tweets

                    cur_tweet = Tweet(tweets[i])
                    tweet_row = cur_tweet.descomposing_tweet(driver)
                    self.tweets = pd_user.append(tweet_row,ignore_index=True)
                    time.sleep(0.2)
                    last_location = tweets[i].location['y']
                    print(self.tweets.shape)

            driver.execute_script("window.scrollBy(0, 1700);")
            time.sleep(1)
            finish_height = driver.execute_script("return document.body.scrollHeight")

            if last_location == previous_location:
                red_flag += 1

            if red_flag > 1:
                print('Reached bottom')
                done = True
                driver.close()
                break

            previous_location = last_location
            self.start_time = end_time

    def stop_crawling_user(self):
        '''
        Checks if we have reach the end of the timeframe that we are crawling
        '''
        if self.start_time >= self.finish_time:
            return True
        else:
            return False

    def _waiting_func(self,driver,my_element_id):
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
        try: #$find_element_by_class_name
            WebDriverWait(driver, 4,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, my_element_id)))
        except : #(NoSuchElementException, TimeoutException)
            print('Loading took too much time, may be not results')

    def _find_start_time(self):
        '''
        Establish as start date the lastest out of the proposed and the joined date
        '''
        if self.joined_date > self.proposed_start_time:
            start_time = self.joined_date
        else:
            start_time = self.proposed_start_time
        return start_time

    def save_tweets(self):
        self.tweets = self.tweets.drop_duplicates()
        self.tweets.to_csv('Users_tweets/' + self.user_tag + '.csv')

    @classmethod
    def init_user(cls,username):

        # Get the date when the user joined Twitter
        joined_date = cls.user_join_date(username)

        return cls(joined_date,username)

    @staticmethod
    def user_join_date(user_tag):
        '''
        Finds the date a user joined to twitter, by getting this date, we avoid the cralwer to
        scrape dates when the user was not even on twotter, makes things faster

        Args:   @input - user_tag of the user e.g.: @realDonalTrump
                @output - datetime variable
        '''
        query = "https://twitter.com/" + str(user_tag)

        #driver = webdriver.Chrome(chrome_driver_binary,options=options)
        driver = webdriver.Chrome(options=options)

        driver.get(query)
        time.sleep(1)
        aa = driver.find_elements_by_css_selector('span.css-901oao.css-16my406.r-m0bqgq.r-4qtqp9.r-1qd0xha.r-ad9z0x.r-zso239.r-bcqeeo.r-qvutc0')
        joined_date = datetime.datetime.strptime(aa[-1].text.replace('Joined ',''), "%B %Y").date()
        return joined_date
