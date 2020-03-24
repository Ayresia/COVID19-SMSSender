# Project: COVID19-SMSSender
# Developer: Ayresia
# Date: 24th March 2020

import requests
import time
import configparser
import os
import sys

from urllib import request
from twilio.rest import Client
from datetime import datetime
from pathlib import Path

config = configparser.ConfigParser()
configuration_file = Path('config.ini')

def get_config(section, key):
    config.read('config.ini')
    return config[section][key]

def check_config():

    if not Path(configuration_file).exists():
        config['TWILIO'] = {'AccountSID': 'null', 'AuthKey': 'null', 'TwilioNumber': 'null'}
        config['API'] = {'Country': 'null', 'PhoneNumbers': 'null'}

        with open('config.ini', 'w') as file:
            config.write(file)
            print("Configuration > I have just created a config.ini, please edit it.")
            sys.exit(1)

    else:
        if any(get_config("TWILIO", i) == "null" for i in ("AccountSID", "AuthKey", "TwilioNumber")):
            print("Configuration > You have something wrong in the TWILIO Section.")
            sys.exit(1)
        elif any(get_config("API", i) == "null" for i in ("PhoneNumbers", "Country")):
            print("Configuration > You have something wrong in the API Section.")
            sys.exit(1)

def send_sms(body_text):
    account_sid = get_config("TWILIO", "AccountSID")
    auth_token = get_config("TWILIO", "AuthKey")

    client = Client(account_sid, auth_token)

    phone_numbers = get_config("API", "PhoneNumbers")
    phone_numbers = phone_numbers.split(',')
    phone_numbers = [p_num.strip(' ') for p_num in phone_numbers]

    twilio_number = get_config("TWILIO", "TwilioNumber")

    for numbers in phone_numbers:
        print('Sending Message to: ' + numbers)

        message = client.messages.create(
            body = body_text,
            from_ = twilio_number,
            to = numbers
        )

        print("Status: " + message.status)

def check_api():

    # Get URL as a JSON
    url_api = "https://coronavirus-19-api.herokuapp.com/countries/" + get_config('API', 'Country')
    data = requests.get(url_api).json()

    old_total_cases = data['cases']

    while True:
        # Get URL as a JSON
        looped_data = requests.get(url_api).json()

        new_total_cases = looped_data['cases']

        if new_total_cases == old_total_cases:
            print('Checking > No Added Cases in ' + get_config('API', 'Country'))
            time.sleep(15)
        else:
            print('Checking > There are new Cases in ' + get_config('API', 'Country') + "!")

            old_total_cases = new_total_cases

            send_sms(f'''
COVID-19 Update:
            
Total Cases: {new_total_cases} 
New Cases: {looped_data["todayCases"]} 
Active Cases: {looped_data["active"]}
            
Total Deaths: {looped_data["deaths"]}
Total Recovered: {looped_data["recovered"]}
Total Critical: {looped_data["critical"]}
            
Date & Time: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
These stats are not 100% accurate, but close enough.''')
            break
