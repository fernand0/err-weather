from errbot import BotPlugin, botcmd
import configparser
import datetime
import json
import requests

from socialModules.configMod import *

class HelloWorld(BotPlugin):

    def loadData(self, typeData = 'weather', city = 'Zaragoza,es'):
    
        config = configparser.ConfigParser()
        config.read(CONFIGDIR + '/.rssOpenWeather')
    
        apiKey=config.get('OpenWeather','api')
    
        urlBase = 'http://api.openweathermap.org/data/2.5/'
        url = f"{urlBase}{typeData}?q={city},&APPID={apiKey}&units=metric"
        weather = requests.get(url)
    
        logging.info(weather.text)
        data = json.loads(weather.text)
    
        return data
    
    def nameToEmoji(self, text):
        # https://openweathermap.org/weather-conditions
        toShow = None
        if text  == 'overcast clouds':
             toShow = '☁️' # ☁️ '
        elif text == 'scattered clouds':
             toShow = '🌥️' 
        elif text == 'few clouds':
             toShow = '🌤️' 
        elif text == 'broken clouds':
             toShow = '🌤️'
        elif text == 'clear sky':
             toShow = '🌞'
        elif text == 'light rain':
             toShow = '🌦️'
        elif text == 'snow':
             toShow = '☃️'
        elif text == 'fog':
             toShow = '🌫️'
    
        return toShow

    @botcmd  # this tag this method as a command
    def weather(self, mess, args):  # it will respond to !hello
        """this command says hello"""  # this will be the answer of !help hello
        dataW = self.loadData('weather', 'Zaragoza,es')
        dataF = self.loadData('forecast')

        yield(f"Now: {self.nameToEmoji(dataW['weather'][0]['description'])}  "
              f"Temp: {dataW['main']['temp']}")

        previousDate = ''
        prediction = {}
        today = datetime.datetime.now()
        lenDate = len('xxxx-xx-xx')
        line = f"{str(today)[:lenDate]}:"
        for dataD in dataF['list']:
            day = dataD['dt_txt'][lenDate-2:lenDate]
            if int(day) == today.day:
                toShow = self.nameToEmoji(dataD['weather'][-1]['description'])
                temp = round(dataD['main']['temp_min'])
                if len(line) == len(day):
                    # No data yet
                    tempMin = temp
                    tempMax = temp
                else:
                    tempMin = min(temp, tempMin)
                    tempMax = max(temp, tempMax)
                temp = str(temp)
                if len(temp) == 1: temp = f" {temp}"
                line = f"{line} {temp} {toShow}"
            else:
                line = f"{line} [{tempMin},{tempMax}]"
                yield(f"{line}")
                today = today + datetime.timedelta(days=1)
                line = f"{str(today)[:lenDate]}:"

