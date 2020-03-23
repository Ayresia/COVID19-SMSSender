# Project: COVID19-SMSSender
# Developer: Ayresia
# Date: 21th March 2020

import requests, time, configparser, os, sys

from urllib import request
from twilio.rest import Client
from datetime import datetime
from pathlib import Path

config = configparser.ConfigParser()
configuration_file = Path('config.ini')

def get_config(section, key):
    config.read('config.ini')
    return config[section][key]

url_api = "https://coronavirus-19-api.herokuapp.com/countries/" + get_config('API', 'Country')

def check_config():
    data = requests.get(url_api).text

    account_sid = get_config("TWILIO", "AccountSID")
    auth_token = get_config("TWILIO", "AuthKey")

    client = Client(account_sid, auth_token)
    client.available_phone_numbers.get(0)
    
    if not Path('config.ini').is_file():
        config['TWILIO'] = {'AccountSID': 'null', 'AuthKey': 'null', 'TwilioNumber': 'null'}
        config['API'] = {'Country': 'null', 'PhoneNumbers': 'null'}

        config.write(configuration_file.open('w'))
    else:
        if any(get_config("TWILIO", i) == "null" for i in ("AccountSID", "AuthKey", "TwilioNumber")):
            print("Configuration > You have something wrong in the TWILIO Section.")
            sys.exit(1)
        elif any(get_config("API", i) == "null" for i in ("PhoneNumbers", "Country")):
            print("Configuration > You have something wrong in the API Section.")
            sys.exit(1)
        elif data == "Country not found":
            print('Configuration > The country is invalid/incorrect.')
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

            today_cases = looped_data['todayCases']
            active_cases = looped_data['active']
            total_deaths = looped_data['deaths']
            total_recovered = looped_data['recovered']
            total_critical = looped_data['critical']
            today_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            send_sms(f'\nCOVID-19 Update:\n\nTotal Cases: {new_total_cases} \nNew Cases: {today_cases} \nActive Cases: {active_cases}\nTotal Deaths: {total_deaths}\nTotal Recovered: {total_recovered}\nTotal Critical: {total_critical}\n\nDate & Time: {today_date}\n\nThese stats are not 100% accurate, but close enough.')
            break
