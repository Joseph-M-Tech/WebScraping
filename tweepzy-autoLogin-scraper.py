#imports
import selenium
import csv
from getpass import getpass
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchAttributeException
# from selenium.webdriver import Chrome

#function
def get_tweet_data(card):
    """Extract from tweet data"""
    username = card.find_element_by_xpath('.//span').text
    handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    try:
        postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
    except NoSuchAttributeException:
        return
    comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text#.strip()
    text = comment + responding
    reply_ctn = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_ctn = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_ctn = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    
    tweet = (username, handle, postdate, text, reply_ctn, retweet_ctn, like_ctn)
    return tweet

#create instance of webdriver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#navigate to login screen
driver.get('https://www.twitter.com/login')
driver.maximize_window()

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys('Harry72426254')

# my_password = getpass()
password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys('30422403josmacmm')
password.send_keys(Keys.RETURN)

#find search input & search for term
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys('@SmascoCare')
search_input.send_keys(Keys.RETURN)

#navigate to 'latest' tab
# selenium.webdriver.support.wait.WebDriverWait()
driver.implicitly_wait(60)
driver.find_element_by_link_text("Latest").click()

#get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.paggeYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
    
    scroll_attempt = 0
    while True:
        #check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)

        curr_position = driver.execute_script("return window.paggeYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            #end scroll region
            if scroll_attempt >=5:
                scrolling = False
                break
            
            else:
                sleep(6) #attempt to scroll again
                
        else:
            last_position = curr_position
            break


#output the data in csv
with open('data_tweet.csv', 'w', newline ='', encoding = 'utf-8') as f:
    header = ['Username', 'Handle', 'Timestamp', 'Comments', 'Likes', 'Retweets', 'Text']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)