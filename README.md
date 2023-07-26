# twitterBot
Twitter bot used python selenium to emulate user. Can reply to target handles using open ai api

Overview

This repository contains a Python-based Twitter bot that leverages Selenium to automate interactions with the Twitter platform. The bot is designed to reply to tweets from targeted @handles capturing the tweets and replies and sending them to chatGPT api to generate a response all using a headless browser.
Requirements

To run the Twitter bot, you need to have the following dependencies installed:

    Python (version 3.6 or later)
    Selenium Python bindings
    WebDriver for your preferred browser (Chrome, Firefox, etc.)

Installation

Clone this repository to your local machine using the following command:
  git clone https://github.com/nateawest/twitterBot.git

Change into the project directory:
  cd twitter-bot

git clone https://github.com/your-username/twitter-bot.git
  pip install -r requirements.txt

Download the appropriate WebDriver for your browser and ensure it is added to your system's PATH.
I used firefox because it has a headless browser if you want to use a different browser you'll need to make changes to the driver within main

Configuration

Before running the Twitter bot, you need to provide your Twitter account credentials, openAi token, and discord token and channel id's if you plan on using discord
I used discord to schedule my replies. add some variability, and send me updates on bots performance

Contributing

If you would like to contribute to this project, you can follow these steps:

    Fork the repository on GitHub.

    Create a new branch with a descriptive name for your feature or bug fix:

    git checkout -b my-new-feature

Make the necessary changes and commit your code.

Push your changes to your forked repository.

Submit a pull request, explaining the changes you have made and why they should be merged.
