import requests, time
import json
import smtplib
import re

speed_threshold = 15
gust_threshold = 20

carriers = {
    'att': '@mms.att.net',
    'tmobile': ' @tmomail.net',
    'verizon': '@vtext.com',
    'sprint': '@page.nextel.com'
}


def send(message):
    # Replace the number with your own, or consider using an argument\dict for multiple people.
    to_number = '**PHONE NUMBER**{}'.format(carriers['att'])
    auth = ('**EMAIL**', '**PASSWORD**')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send text message through SMS gateway of destination number
    server.sendmail(auth[0], to_number, message.encode('utf8'))


# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)
prev_time = ""

while True:
    response = requests.get(
        "https://avwx.rest/api/taf/kprc?options=summary&airport=true&reporting=true&format=json&onfail=cache",
        headers={'Authorization': '**API key**'})

    data = response.json()

    for i in range(0, len(data['forecast'])):

        try:
            speed_int = data['forecast'][i]['wind_speed']['value']
        except TypeError:
            speed_int = 0
        try:
            gust_int = data['forecast'][i]['wind_gust']['value']
        except TypeError:
            gust_int = 0

        if speed_int is not None or gust_int is not None:
            if speed_int > speed_threshold or gust_int > gust_threshold:
                try:
                    weather_time = data['forecast'][i]['end_time']['dt']
                except TypeError:
                    weather_time = "Not found"
                try:
                    speed = str(data['forecast'][i]['wind_speed']['value'])
                except TypeError:
                    speed = "Not found"
                try:
                    gust = str(data['forecast'][i]['wind_gust']['value'])
                except TypeError:
                    gust = "Not found"
                try:
                    direction = str(data['forecast'][i]['wind_direction']['repr'])
                except TypeError:
                    direction = 0

                if weather_time != prev_time:
                    prev_time = weather_time
                    weather_time = re.sub(':', ';', weather_time)
                    text = "Time " + weather_time + "\n" + "Wind speed " + speed + "\n" + "Gust speed " + gust + "\n" + "Direction " + direction
                    #print(text)
                    send(text)

                else:
                    print("Weather has not changed")
    time.sleep(3600)
