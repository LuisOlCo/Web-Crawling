import os
import pandas as pd 

import time
import datetime
from datetime import timedelta
from datetime import date

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


from utils import *

options = Options()
chrome_exe = '/home/luis/data_crawling_elections/chromedriver'
options.add_argument('--headless')
options.add_argument('--disable-gpu')  


def timeTransformation(start_time):
    end_time = start_time + timedelta(days=5)

    start_time_str = str(start_time.year) + '-' + str(start_time.month) + '-' + str(start_time.day)
    end_time_str = str(end_time.year) + '-' + str(end_time.month) + '-' + str(end_time.day)
    print('Period: ' + start_time_str + ' / ' + end_time_str)

    return start_time_str,end_time_str,end_time

def checkingUserAccount(user_tag):
    # checks if the account given exists on twitter still
    query = "https://twitter.com/search?q=(from%3A" + str(user_tag) + ")&src=typed_query"
    driver = webdriver.Chrome(executable_path=chrome_exe,options=options)
    driver.get(query)
    time.sleep(1)
    try:
        aa = driver.find_element_by_css_selector('div.css-1dbjc4n.r-d9fdf6.r-6wcr4z')
        if 'No results for' in aa.text:
            print('Account suspended for ' + user_tag)
            driver.quit()
            return True
    except:
        print('User account not suspended')
        driver.quit()

def userJoinDate(user_tag):
    # checks for the date when the user joined twitter
    query = "https://twitter.com/" + str(user_tag) 
    driver = webdriver.Chrome(executable_path=chrome_exe,options=options)
    driver.get(query)
    time.sleep(1)
    
    aa = driver.find_element_by_css_selector('span.css-901oao.css-16my406.r-1re7ezh.r-4qtqp9.r-1qd0xha.r-ad9z0x.r-zso239.r-bcqeeo.r-qvutc0')
    print(aa.text)
    joined_date = datetime.datetime.strptime(aa.text.replace('Joined ',''), "%B %Y").date()
    return joined_date

def getSuspendedAccounts():
    lista = []
    with open('suspended_accounts.txt') as f:
        for line in f:
            print(line)
            lista.append(line.strip())
    f.close()
    return lista

def accountProtected(driver):
    state = driver.find_element_by_css_selector('div.css-901oao.r-hkyrab.r-1qd0xha.r-1b6yd1w.r-b88u0q.r-ad9z0x.r-15d164r.r-bcqeeo.r-q4m81j.r-qvutc0')
    print(state.text)
    if 'protected' in state.text:
        return True
    else:
        return False

def main():

    list_suspended_accounts = getSuspendedAccounts()

    pending_users = pd.read_csv('depressed_username_and_userid.csv')

    for user_tag in list(pending_users['username']):

        #Evaluate Users:
            # 1.- Account has been suspended
            # 2.- When did open the account

        # Check first that the usr account exists and if we have evaluated this user already
        if not os.path.isfile('Users_tweets/' + user_tag + '.csv' ) and user_tag not in list_suspended_accounts:
            
            if not checkingUserAccount(user_tag):

                pd_user = pd.DataFrame(columns=['Username','User_tag','Date','Tweet','Replies','Retweets','Likes','Retweet'])
                print(user_tag)

                # Before start crawling check, when the user joined to start crawling from that date
                #joined_date = userJoinDate(user_tag)
                finish_time = date(2020,11,13) 
                #proposed_start_time = date(2020,11,3)  # election date
                start_time = date(2020,11,3)

                # this is the date from which we are starting to crawl the data
                #if joined_date > proposed_start_time:
                #    start_time = joined_date
                #else:
                #    start_time = proposed_start_time

                
                # while start_time and finish_time are different, keep crawling
                while True:
                    
                    start_time_str,end_time_str,end_time = timeTransformation(start_time)
                    # Access to Twitter
                    query = 'https://twitter.com/search?q=(from%3A' + user_tag + ')%20until%3A'+ end_time_str + '%20since%3A' + start_time_str + '&src=typed_query'
                    driver = webdriver.Chrome(executable_path=chrome_exe,chrome_options=options)
                    print(query)
                    driver.get(query)

                    #if accountProtected(driver):
                    #    break
                    try: 
                        pd_user = retrievingTweetsFromUser(driver,pd_user)
                        start_time = end_time

                        if start_time >= finish_time:
                            break
                    except:
                        break
                
                # save the users tweets
                pd_user = pd_user.drop_duplicates()
                pd_user.to_csv('Users_tweets/' + user_tag + '.csv')
            
            else:
                with open('suspended_accounts.txt', 'a') as f:
                    f.write(user_tag + '\n')
                f.close()


        else:
            if os.path.isfile('Users_tweets/' + user_tag + '.csv' ):
                print('User already scrapped')

            elif user_tag in list_suspended_accounts:
                print('User account in black list')
               

if __name__ == "__main__":
    main()