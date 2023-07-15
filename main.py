import os
import time
import openai
import random
import discord
from discord.ext import commands, tasks
from datetime import datetime
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
openai.api_key = os.getenv("OPENAI_TOKEN")
twit_name = os.getenv('TWIT_NAME')
twit_pass = os.getenv('TWIT_PASS')
twit_user = os.getenv('TWIT_USER')


def open_twitter(driver):
    # extra step variable for bot check
    botCheck = 'There was unusual login activity on your account. To help keep your account safe, please enter your phone number or username to verify it’s you.'
    # open twitter
    driver.get('https://twitter.com/login')
    time.sleep(5)  # Wait for the page to load
    # Click on the "Use phone / email / username" link
    username_field = driver.find_element(By.XPATH,
                                         '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username_field.click()
    # Enter your username
    username_field.send_keys(twit_name)
    # Click on the "Log in" button
    login_button = driver.find_element(By.XPATH,
                                       '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    login_button.click()

    time.sleep(5)  # Wait for the page to load


    # twitter notices unusual login activity. This is a extra middle step login using your handle. Using try incase it doesn't notice unusual activity
    try:
        # Find the element using XPath
        element = driver.find_element(By.XPATH,
                                      '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div/span/span')
        # Get the text from the element
        text = element.text
        # Print the captured string
        print("Captured String:", text)
        if text == botCheck:
            bot_field = driver.find_element(By.XPATH,
                                            '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
            bot_field.send_keys(twit_user)
            bot_field_button = driver.find_element(By.XPATH,
                                                   '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div/span/span')
            bot_field_button.click()

    # no activity check login using these xpaths
    except Exception as e:
        print("An error occurred:", str(e))
        print("no check")
        password_field = driver.find_element(By.XPATH,
                                             '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        password_field.send_keys(twit_pass)
        password_button = driver.find_element(By.XPATH,
                                              '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div/span/span')
        password_button.click()
    # 3rd step input password. Different xpath unusual activity vs not
    password_field2 = driver.find_element(By.XPATH,
                                          '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
    password_field2.send_keys(twit_pass)
    password_button2 = driver.find_element(By.XPATH,
                                           '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
    password_button2.click()

    return


def search_twitter(driver, search_query):
    # click on search
    search_field = driver.find_element(By.XPATH,
                                       '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    # enter search query
    search_field.send_keys(search_query)
    search_field.send_keys(Keys.RETURN)
    # Wait for the page to load (you may need to adjust the wait time)
    time.sleep(5)
    # Click on the user profile link. Finds the path via handle
    user_profile_link = driver.find_element(By.XPATH, "//span[contains(text(), '" + search_query + "')]")
    user_profile_link.click()
    driver.implicitly_wait(5)


# down
def scroll(driver):
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.PAGE_DOWN)


def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")


def pinned_tweets(driver):

    # I wanted to ignore pinned tweets because they do not change often
    time.sleep(3)
    try:
        # Locate the span element containing the text
        span_element = driver.find_element(By.XPATH, "//span[contains(@class, 'css-901oao') and text()='Pinned Tweet']")
        # Check if the tweet is pinned
        is_pinned = True if span_element else False
        # Print the result if the tweet is pinned
        if is_pinned:
            print("This tweet is pinned.")
            return 1
    except:
        print("This tweet is not pinned.")
        return 0


def used_tweet(target_string):
    # checks if the tweet has been stored in file. Do not want to reply twice
    try:
        file_path = os.path.join(os.path.dirname(__file__), 'usedtweet.txt')
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if target_string in line:
                    print("Tweet is used, skip")
                    return True
        return False
    except IOError:
        print("Error: Unable to read the file.")
        return False


def store_tweet(target_string):
    # This is important to insure we do not reply twice
    file_path = os.path.join(os.path.dirname(__file__), 'usedtweet.txt')
    print("file_path I'm trying to access:" , file_path)
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(target_string + '\n')
        print("String successfully stored in the file.")
    except IOError:
        print("Error: Unable to write to the file.")


def like_home_page(driver):
    tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")
    captured_elements = []  # store the element to get a user reply count on tweet

    # Find and capture initial tweets
    tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")
    # Scroll and capture more tweets
    for _ in range(3):
        # Scroll to the bottom of the page
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)  # Wait for the page to load after scrolling
        # Find and capture newly loaded tweets
        tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")

    # lets like a few post in our feed to make us look more human
    like_counter = 0
    for i in range(3):
        driver.execute_script("arguments[0].scrollIntoView();", tweet_elements[like_counter])
        like_element = tweet_elements[like_counter].find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/div/section/div/div/div/div/div[2]/div/div/article/div/div/div[2]/div[2]/div[4]/div/div[3]/div/div/div[2]/span/span/span")
        like_element.click()
        like_counter += random.randint(0, 2)
        time.sleep(2)


def reply_to_tweets(driver, search_query):
    # use search bar
    search_twitter(driver, search_query)
    # page needs a chance to load between methods
    driver.implicitly_wait(2)
    # check if the first tweet is pinned, we don't want to respond to a pinned tweet
    pin_check = pinned_tweets(driver)

    tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")
    # three arrays
    captured_tweets = []    # store text content
    captured_links = []     # store link so we can come back and click tweet
    captured_elements = []  # store the element to get a user reply count on tweet

    # trying to capture tweet, link, and element and append to array. If no element present pass
    for tweet_element in tweet_elements:
        try:
            tweet_text_element = tweet_element.find_element(By.XPATH, ".//div[@lang='en']")
            tweet_text = tweet_text_element.text
            #
            captured_tweets.append(tweet_text)
            tweet_link = tweet_element.find_element(By.XPATH, ".//a[contains(@href, '/status/')]")
            captured_links.append(tweet_link)
            captured_elements.append(tweet_element)
        except NoSuchElementException:
            pass

    scroll(driver)  # Call scroll function

    # trying to capture tweet, link, and element and append to array. If no element present pass
    tweet_elements = driver.find_elements(By.XPATH, "//article[contains(@data-testid, 'tweet')]")
    for tweet_element in tweet_elements:
        try:
            tweet_text_element = tweet_element.find_element(By.XPATH, ".//div[@lang='en']")
            tweet_text = tweet_text_element.text
            if tweet_text not in captured_tweets:
                captured_tweets.append(tweet_text)
            if tweet_text_element not in captured_elements:
                tweet_link = tweet_element.find_element(By.XPATH, ".//a[contains(@href, '/status/')]")
                captured_links.append(tweet_link)
                captured_elements.append(tweet_element)
        except NoSuchElementException:
            pass

    # if the first tweet was market as pinned we will just start iterating through array at index 1
    i_counter = 0
    if pin_check == 1:
        i_counter += 1
    size = len(captured_tweets)

    comment_count_int = 0
    while i_counter < size:
        # get the number of replies/comments
        comment_element = captured_elements[i_counter].find_element(By.XPATH, ".//div[@data-testid='reply']")
        comment_count_str = comment_element.get_attribute("aria-label")
        numeric_part = ''.join(filter(str.isdigit, comment_count_str))
        comment_count_int = int(numeric_part)
        print("current tweet inspection:", captured_tweets[i_counter])
        # Skip tweets we've already replied to:
        if not used_tweet(captured_tweets[i_counter]):
            break
        i_counter += 1
    if i_counter == size: # we went through the whole array and all the tweets have be replied to
        print("No post with enough replies/no new replies to make")
        return
    captured_links[i_counter].click()
    time.sleep(3)

    # capture replies logic
    replies = []
    result = False
    old_height = driver.execute_script("return document.body.scrollHeight")

    # set initial all_tweets to start loop
    all_replies = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

    while not result:

        for item in all_replies[0:]:  # skip tweet already scrapped
            try:
                text = item.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
            except:
                text = '[empty]' # sometimes you'll catch empty replies which causes coding errors
            # Append new replies to array
            replies.append([text])
        # scroll down the page
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == old_height:
            result = True
        old_height = new_height
        # update all_replies to keep loop
        all_replies = driver.find_elements(By.XPATH, '//div[@data-testid]//article[@data-testid="tweet"]')

        # make sure there are not more index than there were replies (captured extra stuff)
        del replies[0]
        replies_size = len(replies)
        if comment_count_int < replies_size:
            replies = replies[:comment_count_int]

        flattened_list = [str(item) for sublist in replies for item in sublist]
        combined_replies = '\n'.join(flattened_list)
        reply_to_tweet = captured_tweets[i_counter]

        # call open ai function to get chatGPT to help us generate a response off of tweet and replies
        open_ai_response = send_openai(search_query, reply_to_tweet, combined_replies, comment_count_int)
        print("ChatGPT:   ", open_ai_response)

        # scroll back to top of screen so reply is visible
        scroll_to_top(driver)
        time.sleep(1)
        # enter our reply and submit
        # took a while to find the correct css selector
        reply_field = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')
        reply_field.click()
        reply_field.send_keys(open_ai_response)
        reply_field.send_keys(Keys.RETURN)
        time.sleep(2)
        reply_button = driver.find_element(By.CSS_SELECTOR, 'div.r-42olwf:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)')
        # reply_button.click()
        # store tweet function so that we don't reply to same tweet more than once
        store_tweet(captured_tweets[i_counter])
        # putting together a discord update string
        return_str = "Tweet: " + reply_to_tweet + "\n\nMy response: " + open_ai_response
        driver.get('https://twitter.com/home')
        return return_str


def send_openai(search_query, target_tweet, example_replies, reply_counter):
    MAX_RETRIES = 10
    RETRY_DELAY = 5
    # Info for openai. I stored some background info on tweet targets in the .env file
    back_ground = ""
    if search_query == '@blckriflecoffee':
        back_ground = 'RIFLE'
        print("got background")
    elif search_query == '@verge':
        back_ground = 'VERGE'
    elif search_query == '@NintendoAmerica':
        back_ground = 'NINTENDO'
    elif search_query == '@dallasmavs':
        back_ground = 'MAVS'
    elif search_query == '@MarketWatch':
        back_ground = 'MARKETWATCH'
    elif search_query == '@REI':
        back_ground = 'REI'
    elif search_query == '@SpaceX':
        back_ground = 'SPACEX'
    elif search_query == '@elonmusk':
        back_ground = 'ELON'

    # get strings stored in .env file
    rules_str = os.getenv('RULES')
    replies_str = os.getenv('REPLIES')
    tweet_str = os.getenv('TWEETINFO')
    back_ground_str = os.getenv(back_ground)

    the_str = rules_str + back_ground_str
    # if we had a decent number of user replies we can get chatGPT to consider those while formulating response
    if reply_counter > 3:
        the_str += tweet_str + target_tweet + replies_str + example_replies
    else:   # if not enough replies we want to leave that out of our chatGPT request or it sometimes confuses it
        the_str += tweet_str + target_tweet

    # sometimes chatGPT api is busy and we to wait a few seconds
    retries = 0
    while retries < MAX_RETRIES:
        try:
            # Generate a response using ChatGPT
            chat_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an helpful assistant."},
                    {"role": "user", "content": the_str}
                ]
            )
            return chat_response.choices[0].message.content
        except openai.error.ServiceUnavailableError:
            time.sleep(RETRY_DELAY)
            retries += 1
    raise Exception("Failed to get a response.")


def discord_bot():

    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.message_content = True  # Enable the message content intent

    rules_str = os.getenv('RULES')
    channel_id = os.getenv('CHANNELID')           # one channel to post the tweet and my response
    channel_live = os.getenv('CHANNELLIVE')       # one channel to update me on status of bot
    bot = commands.Bot(command_prefix='!', intents=intents)
    # first post time will be at 9 am, but it'll change each day at midnight
    first_post_time = 20
    second_post_time = 22
    have_posted = 0
    bool_2 = False
    reply_counter = 0
    target_counter = 0

    # Create a loop task for every 27 minutes. The odd loop time will give my tweets more variable post times
    # I used discord as my post scheduler and to get me informed on the bots replies and status
    @tasks.loop(minutes=27)
    async def send_message(post_time, post_time2, have_i_posted, post_bool, reply_counter_v, target_counter_v):
        channel = bot.get_channel(int(channel_id))
        channel_live_status = bot.get_channel(int(channel_live))
        # update us on the status of the bot
        await channel_live_status.send("Live, current post time: " + str(post_time) + " and " + str(post_time2))
        # we will use the hour to decide when to tweet
        current_time = datetime.now().time().strftime("%H")
        # tweet targets and counter
        tweet_target = ['@verge', '@blckriflecoffee', '@NintendoAmerica', '@dallasmavs', '@MarketWatch', '@REI', '@SpaceX', '@elonmusk']

        # we will reset post time at midnight every night
        if int(current_time) == 22 and not post_bool:
            post_time = random.randint(9, 16)
            post_time2 = post_time + random.randint(1, 5)
            have_i_posted = 0
        # like some tweets to look more human
        if int(current_time) == post_time - 1:
            fox_driver = webdriver.Firefox(service=s)
            try:
                open_twitter(fox_driver)
                time.sleep(2)
                like_home_page(fox_driver)
                fox_driver.close()
            except:
                pass
            fox_driver.close()

        # first post time of the day
        if int(current_time) == post_time and have_i_posted < 2:
            if target_counter_v == 7:
                target_counter_v = 0
            fox_driver = webdriver.Firefox(service=s)
            open_twitter(fox_driver)
            time.sleep(2)
        # if the post fails still increment have i posted so we don't end up posting twice at same time for post time 2
            try:
                my_tweet = reply_to_tweets(fox_driver, tweet_target[target_counter_v])
                await channel.send(my_tweet)
            except:
                have_i_posted += 1
                pass
            have_i_posted += 1
            post_bool = False
            target_counter_v += 1
            fox_driver.close()

        # post time 2
        if int(current_time) == post_time2 and have_i_posted < 2:
            if target_counter_v == 7:
                target_counter_v = 0
            fox_driver = webdriver.Firefox(service=s)
            open_twitter(fox_driver)
            time.sleep(2)
            try:
                my_tweet = reply_to_tweets(fox_driver, tweet_target[target_counter_v])
                await channel.send(my_tweet)
            except:
                have_i_posted += 1
                pass
            have_i_posted += 1
            target_counter_v += 1
            fox_driver.close()

        # like tweets x2
        if int(current_time) == post_time + 1:
            fox_driver = webdriver.Firefox(service=s)
            try:
                open_twitter(fox_driver)
                time.sleep(2)
                like_home_page(fox_driver)
            except:
                pass
            fox_driver.close()

    @bot.event
    async def on_ready():
        print(f"Bot is ready!")
        send_message.start(first_post_time, second_post_time, have_posted, bool_2, reply_counter, target_counter)

    # await channel.send(message1)
    # await channel.send(message2)
    # await bot.close()
    bot.run(discord_token)


# In order to create our driver lets first create a service object
s = Service(GeckoDriverManager().install())
# The discord bot function acts as my bot scheduler and updates me
discord_bot()

