# Project: COVID19-SMSSender
# Developer: Ayresia
# Date: 21th March 2020

import json, urllib.request, time, configparser, os
from twilio.rest import Client
from datetime import datetime

config = configparser.ConfigParser()

def sendSMS(bodyText):
    account_sid = getConfig("TWILIO", "AccountSID")
    auth_token = getConfig("TWILIO", "AuthKey")

    try:
        client = Client(account_sid, auth_token)
    except:
        print("Configuration > Your AccountSID or AuthToken is invalid/incorrect.")

    phoneNumbers = getConfig("API", "PhoneNumbers")
    phoneNumbers = phoneNumbers.split(',')
    phoneNumbers = [x.strip(' ') for x in phoneNumbers]

    twilioNumber = getConfig("TWILIO", "TwilioNumber")

    for numbers in phoneNumbers:
        print('Sending Message to: ' + numbers)
        message = client.messages.create(
            body = bodyText,
            from_ = twilioNumber,
            to = numbers)
        print("Status: " + message.status)

def checkConfig():

    if not os.path.exists('config.ini'):
        config['TWILIO'] = {'AccountSID': 'null','AuthKey': 'null', 'TwilioNumber': 'null'}
        config['API'] = {'Country': 'null', 'PhoneNumbers': 'null'}
        config.write(open('config.ini', 'w'))
    else:
        if getConfig("TWILIO", "AccountSID") == "null" or getConfig("TWILIO", "AuthKey") == "null" or getConfig("TWILIO", "TwilioNumber") == "null":
            print("Configuration > You have something wrong in the TWILIO Section.")
            os._exit(1)
        if getConfig("API", "Country") == "null" or getConfig("API", "PhoneNumbers") == "null":
            print("Configuration > You have something wrong in the API Section.")
            os._exit(1)

def getConfig(section, key):
    config.read('config.ini')
    return config[section][key]

def checkAPI():

    # Download JSON & Decode.
    urlAPI = "https://coronavirus-19-api.herokuapp.com/countries/" + getConfig('API', 'Country')
    data = urllib.request.urlopen(urlAPI).read().decode()
    if data == "Country not found":
        print("Configuration > That country does not exist.")
        os._exit(1)
    else:
        # Parse JSON Object.
        object = json.loads(data)

        oldTotalCases = 7

        while True:
            # Download JSON & Decode.
            urlAPI1 = "https://coronavirus-19-api.herokuapp.com/countries/" + getConfig('API', 'Country')
            data1 = urllib.request.urlopen(urlAPI1).read().decode()
            object1 = json.loads(data1)

            newTotalCases = str(object1['cases'])

            if newTotalCases == oldTotalCases:
                print('Checking > No Added Cases in ' + getConfig('API', 'Country'))
                time.sleep(15)
            else:
                print('Checking > There are new Cases in ' + getConfig('API', 'Country') + "!")

                oldTotalCases = newTotalCases

                todayCases = str(object['todayCases'])
                activeCases = str(object['active'])
                totalDeaths = str(object['deaths'])
                totalRecovered = str(object['recovered'])
                totalCritical = str(object['critical'])
                todayDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                sendSMS('\nCOVID-19 Update:\n\nTotal Cases: ' + newTotalCases + '\nNew Cases: ' + todayCases + '\nActive Cases: ' + activeCases + '\nTotal Deaths: ' + totalDeaths + '\nTotal Recovered: ' + totalRecovered + '\nTotal Critical: ' + totalCritical + "\n\nDate & Time: " + todayDate)
                break