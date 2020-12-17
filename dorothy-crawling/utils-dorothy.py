
import time
import datetime
from datetime import timedelta
from datetime import date

import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def checkTweets(driver):

    #try:
        css_results = 'div.css-901oao.r-18jsvk2.r-1qd0xha.r-1b6yd1w.r-b88u0q.r-ad9z0x.r-15d164r.r-bcqeeo.r-q4m81j.r-qvutc0'
        aa = driver.find_element_by_css_selector(css_results)
        if 'No results for' in aa.text:
            print('FUNCTION: NO TWEETS FOR THIS PERIOD OF TIME')
            return False
            # jump to the next set of days
    #except:
        # In cases there are tweets the search for the css elements with derive an error
        #print('FUNCTION: THERE ARE TWEETS')
        #return True

def descomposingTweet(tweet,pd_user,driver):


    abb = {'Jan':'January', 'Feb':'February','Mar': 'March','Apr': 'April', 'May':'May','Jun':'June','June':'June',
       'Jul':'July','July':'July', 'Aug':'August','Sep':'September', 'Sept': 'September','Oct': 'October',
       'Nov': 'November','Dec':'December'}

    #username
    time.sleep(0.2)
    css_username = 'div.css-901oao.css-bfa6kz.r-18jsvk2.r-1qd0xha.r-a023e6.r-b88u0q.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
                 # 'div.css-901oao.css-bfa6kz.r-hkyrab.r-1qd0xha.r-a023e6.r-b88u0q.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
    css_user_tag = 'div.css-901oao.css-bfa6kz.r-m0bqgq.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
                 # 'div.css-901oao.css-bfa6kz.r-1re7ezh.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
    css_tweet = 'div.css-901oao.r-18jsvk2.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'
              # 'div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0'
    css_date =  'a.css-4rbku5.css-18t94o4.css-901oao.r-m0bqgq.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0'
              # 'a.r-1re7ezh.r-1loqt21.r-1q142lx.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-3s2u2q.r-qvutc0.css-4rbku5.css-18t94o4.css-901oao'
    css_retweet = 'a.css-4rbku5.css-18t94o4.css-901oao.r-m0bqgq.r-1loqt21.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
                # 'a.css-4rbku5.css-18t94o4.css-901oao.r-1re7ezh.r-1loqt21.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0'
    waiting_func(driver,css_username)
    username = tweet.find_element_by_css_selector(css_username).text
    waiting_func(driver,css_user_tag)
    user_tag = tweet.find_element_by_css_selector(css_user_tag).text

    # Text
    try:
        waiting_func(driver,css_tweet)
        text = tweet.find_element_by_css_selector(css_tweet).text
    except:
        text = 'No text'

    # Date
    waiting_func(driver,css_date)
    date_ob = tweet.find_element_by_css_selector(css_date)
    tweet_date = date_ob.get_property('title')

    '''
    Previous version
    date_fil = date_ob.get_property('title').replace('AM','').replace('PM','').replace(' · ','')
    for key,value in abb.items():
        if key in date_fil:
            #raw_date = date_fil.replace(key,value)
            last_date = datetime.datetime.strptime(date_fil.replace(key,value), "%H:%M %B %d, %Y")
            break
    '''
    date_ob = tweet.find_element_by_css_selector('div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2')
    ad = date_ob.find_elements_by_tag_name("time")
    #attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', ad[0])
    last_date = datetime.datetime.strptime(ad[0].get_attribute('datetime'), "%Y-%m-%dT%H:%M:%S.000Z")



    # Replies, Retweets & Likes
    waiting_func(driver,"div[data-testid='reply']")
    replies = tweet.find_element_by_css_selector("div[data-testid='reply']").text
    retweets = tweet.find_element_by_css_selector("div[data-testid='retweet']").text
    likes = tweet.find_element_by_css_selector("div[data-testid='like']").text


    # Retweet?
    waiting_func(driver,css_retweet)
    try:
        if 'Retweeted' in tweet.find_element_by_css_selector(css_retweet).text:
            retweet = True
        else:
            retweet = False
    except:
        retweet = False

    tweet_row = {'Username':username,'User_tag':user_tag,'Date':last_date,'Tweet':text,'Replies':replies,'Retweets':retweets,'Likes':likes,'Retweet':retweet}

    pd_user = pd_user.append(tweet_row,ignore_index=True)

    print('########')
    print('Username: ',username)
    print('User Tag: ',user_tag)
    print('Text: ',text)
    print('Date: ',last_date)
    print('Replies: ',replies)
    print('Retweets: ',retweets)
    print('Likes: ',likes)
    print('Retweet: ',retweet)

    return last_date,pd_user

def retrievingTweetsFromUser(driver,pd_user):
    times = 0
    previous_location = None
    red_flag = 0
    done = False
    last_location = 0
    while True:
        print('**********************')
        print('While Loops: ',times)
        print('**********************')

        # Check if there are tweets for this period of time
        print('CHECKING IF THERE ARE TWEETS:')
        if not checkTweets(driver):
            print('NO TWEETS FOR THIS PERIOD OF TIME')
            break
        else:
            print('THERE ARE TWEETS')

        times += 1

        init_height = driver.execute_script("return document.body.scrollHeight")

        suma = 0
        time.sleep(0.2)

        waiting_func(driver,'div.css-1dbjc4n.r-j7yic.r-qklmqi.r-1adg3ll.r-1ny4l3l')
        aa = driver.find_elements_by_css_selector('div.css-1dbjc4n.r-j7yic.r-qklmqi.r-1adg3ll.r-1ny4l3l')
        # 'div.css-1dbjc4n.r-my5ep6.r-qklmqi.r-1adg3ll.r-1ny4l3l'

        print('elements: ',len(aa))
        if len(aa) > 0:
            for i in range(len(aa)):
                print(i)
                last_date,pd_user = descomposingTweet(aa[i],pd_user,driver)
                time.sleep(0.5)
                last_location = aa[i].location['y']
                suma += aa[i].size['height']
                print('Location item: ',aa[i].location['y'])
                print('Size of the item: ',aa[i].size['height'])
                print(pd_user.shape)
        #print('$$$$$$$')
        #print('Init_height: ',init_height)
        #print('Last location: ',last_location)

        #driver.execute_script("window.scrollTo("+str(aa[i].location['x'])+", "+str(aa[i].location['y'])+");")
        #driver.execute_script("window.scrollTo({top:"+str(aa[i].location['y'])+", left:0});")
        #driver.execute_script("window.scrollBy(0,"+str(suma)+");")
        driver.execute_script("window.scrollBy(0, 1700);")

        time.sleep(1)
        finish_height = driver.execute_script("return document.body.scrollHeight")
        #print('Finish Height: ',finish_height)
        #print('$$$$$$$')


        if last_location == previous_location:
            red_flag += 1

        if red_flag > 1:
            print('Reached bottom')
            done = True
            driver.close()
            break

        previous_location = last_location
        #if init_height >= finish_height:
        #   print('finish')
        #  driver.close()
        # break

        #if last_date < datetime.datetime(2019, 10, 1):
        #    print('Period of time covered')
        #    driver.close()
        #    break

    return pd_user

def waiting_func(driver,my_element_id):
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
    try: #$find_element_by_class_name
        WebDriverWait(driver, 4,ignored_exceptions=ignored_exceptions).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, my_element_id)))
    except : #(NoSuchElementException, TimeoutException)
        print('Loading took too much time, may be not results')
