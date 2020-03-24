# COVID19-SMSSender
Allows you to receive a text-message in real-time whenever there is more Total Cases in that selected Country.

# Screenshots
<a href="url"><img src="https://i.imgur.com/pXGl8oE.png" height="400" width="500" ></a>

# Requirements
- Twilio Account [LINK](https://www.twilio.com/login)

# How to Install
- Run in Command Prompt the following: **pip install -r requirements.txt**
- Edit **config.ini** to your preferable needs.
- Run main.py

# Configuration

```ini
[TWILIO]
accountsid = null
authkey = null
twilionumber = null

[API]
country = null
phonenumbers = null
```
**Twilio Section**:

You can find the **AccountSID**, **AuthKey** and the **Twilio Number** at [Here](https://www.twilio.com/console)

**API Section**:

**Country** - The API I use which is [API Link](https://coronavirus-19-api.herokuapp.com/countries/) has total of **196 countries**, if you have any issue you can always go in the [API Link](https://coronavirus-19-api.herokuapp.com/countries/) and check because the **Country Name** might be instead the **Country Code** like **United States** & **United Kingdom** in the API is actually **US** & **UK**.

**PhoneNumbers** - has to be formatted this way below vv
```
+12025550108,+12025550128,+441632960285,+441632960058
```
It must include the **Dialing Code** for example **UK:** **+44** & **US: **+1** and also the other numbers. After you must put a comma (If you want to add more phone numbers).
