import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
from User import *

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

chrome_driver_binary = '/usr/bin/chromedriver'
chrome_exe = '/home/ec2-user/chromedriver'

def getSuspendedAccounts():
    lista = []
    with open('suspended_accounts.txt') as f:
        for line in f:
            print(line)
            lista.append(line.strip())
    f.close()
    return lista

def pendingAccounts(file):
    lista = []
    with open(file) as f:
        for line in f:
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

def checkingUserAccount(user_tag):
    '''Checks username account
    Args: @input - username that we are studying
          @output - returns True if user account does not exist
    '''

    query = 'https://twitter.com/' + str(user_tag)
    #driver = webdriver.Chrome(chrome_driver_binary,options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(query)
    time.sleep(1)

def main():


    list_suspended_accounts = getSuspendedAccounts()
    pending_users = pd.read_csv('pending_users_luis.csv')['username'].tolist()

    for user_tag in list(pending_users):
        print('New user:' + user_tag)
        if not os.path.isfile('Users_tweets/' + user_tag + '.txt' ) and user_tag not in list_suspended_accounts:

            if not checkingUserAccount(user_tag):
                cur_user = User.init_user(user_tag)
                while True:
                    # Get the dates for which we are going to make the query
                    start_time_str,end_time_str,end_time = cur_user.get_timeframe_for_crawling()
                    query = 'https://twitter.com/search?q=(from%3A' + cur_user.user_tag + ')%20until%3A'+ end_time_str + '%20since%3A' + start_time_str + '&src=typed_query'
                    #driver = webdriver.Chrome(chrome_driver_binary,chrome_options=options)
                    driver = webdriver.Chrome(chrome_options=options) # --> for windows
                    print(query)
                    driver.get(query)
                    try:
                        cur_user.retrieving_tweets_from_user(driver,end_time)
                        if cur_user.stop_crawling_user():
                            break
                    except:
                        break
                cur_user.save_tweets()
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
