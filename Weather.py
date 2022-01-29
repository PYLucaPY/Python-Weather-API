import math
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from time import time, sleep

'''
For this to work you must download a chrome webdriver and selenium and bs4
https://chromedriver.storage.googleapis.com/index.html?path=97.0.4692.71/
'''

class Weather (object):
    def __init__ (self, location):
        self.initializedWithSuccess = False
        self.init_chrome()
        self.weatherURLPass = f"https://www.google.com/search?q=weather+{location}"
        self.init_data()

    def init_chrome (self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.chrome = webdriver.Chrome (options=options)

    def init_data (self):
        try:
            self.chrome.get (self.weatherURLPass)
            sleep(0.05)
            raw = self.chrome.page_source
            html = soup (raw, "html.parser")

            span = html.find_all ('span')
            temperature_tag = html.find_all ('span', {'id':'wob_tm'})
            self.temperature = int(temperature_tag[0].text)
            weather_status_tag = html.find_all ('span', {'id':'wob_dc'})
            self.weather_status = weather_status_tag[0].text
            precipitation_tag = html.find_all ('span', {'id':'wob_pp'})
            self.precipitation = int(precipitation_tag[0].text[:-1])
            humidity_tag = html.find_all ('span', {'id':'wob_hm'})
            self.humidity = int(humidity_tag[0].text[:-1])
            wind_speed_tag = html.find_all ('span', {'id':'wob_ws'})
            self.wind_speed = int(wind_speed_tag[0].text.split(' ')[0])
            location_tag = html.find_all ('div', {'id':'wob_loc'})
            self.location = location_tag[0].text

            parent_temperature_bounds_tag = html.find_all ('div', {'class':'wNE31c'})[0]
            parent_temperature_bounds_tag = parent_temperature_bounds_tag.findChildren ('div', recursive=False)
            self.high_temperature = int(parent_temperature_bounds_tag[0].findChildren ('span', recursive=False)[0].text)
            self.low_temperature = int(parent_temperature_bounds_tag[1].findChildren ('span', recursive=False)[0].text)
            self.initializedWithSuccess = True
        except:
            print ("Invalid location.")
    def terminate (self):
        self.chrome.close()

    def __str__ (self):
        if not self.initializedWithSuccess:
            return ""

        result = ""
        result += (f"Location: {self.location}") + "\n"
        result += (f"Current Temperature: {self.temperature}") + "\n"
        result += (f"Currently: {self.weather_status}") + "\n"
        result += (f"Chance of rain: {self.precipitation}%") + "\n"
        result += (f"Wind with speeds of: {self.wind_speed} mph") + "\n"
        result += (f"Humidity: {self.humidity}%") + "\n"
        result += (f"High of: {self.high_temperature}") + "\n"
        result += (f"Low of: {self.low_temperature}")

        return result
