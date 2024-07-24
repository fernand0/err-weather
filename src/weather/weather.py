from errbot import BotPlugin, botcmd
import configparser
import datetime
import json
import requests

from socialModules.configMod import *

class Weather(BotPlugin):

    def get_configuration_template(self):
        """
            Configuration of the city
        """
        config = {'city': "Zaragoza,es"}
        return config

    def _check_config(self, option):

        # if no config, return nothing
        if self.config is None:
            return None
        else:
            # now, let's validate the key
            if option in self.config:
                return self.config[option]
            else:
                return None

    def activate(self):
        super().activate()

    def loadData(self, typeData = 'weather', city = None):

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
        toShow = text
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
        elif text == 'moderate rain':
            toShow = '🌧️'
        elif text == 'light snow':
             toShow = '🌨️'
        elif text == 'snow':
             toShow = '☃️'
        elif text == 'fog':
             toShow = '🌫️'
    
        return toShow

    @botcmd  # this tag this method as a command
    def weather(self, mess, args):  # it will respond to !hello
        """this command says hello"""  # this will be the answer of !help hello
        city = None
        if args:
            city = args
        if not city:
            city = self._check_config('city')
    
        dataW = self.loadData('weather', city)
        dataF = self.loadData('forecast', city)

        yield(f"Now in {city}: "
              f"{self.nameToEmoji(dataW['weather'][0]['description'])}  "
              f"Temp: {dataW['main']['temp']}")

        previousDate = ''
        prediction = {}
        today = datetime.datetime.now()
        #line = f"{str(today)[:lenDate]}:"
        line = f"{today.strftime('%A')[:1]}:"
        lenDate = len('xxxx-xx-xx')
        tempMin = tempMax = ""
        for dataD in dataF['list']:
            day = dataD['dt_txt'][lenDate-2:lenDate]
            toShow = self.nameToEmoji(dataD['weather'][-1]['description'])
            temp = round(dataD['main']['temp_min'])
            if int(day) == today.day:
                if len(line) == 2:
                    # No data yet
                    tempMin = temp
                    tempMax = temp
                else:
                    if temp and tempMin:
                        tempMin = min(temp, tempMin)
                        tempMax = max(temp, tempMax)
                    else:
                        tempMin = tempMax = temp
                temp = str(temp)
                if len(temp) == 1: temp = f" {temp}"
            else:
                if tempMin or tempMax:
                    # There was a problem when tempMin was 0 (zero)
                    line = f"{line} [{tempMin},{tempMax}]"
                yield line
                today = today + datetime.timedelta(days=1)
                line = f"{today.strftime('%A')[:1]}:"
            line = f"{line} {temp} {toShow}"

        line = f"{line} [{tempMin},{tempMax}]"
        yield(f"{line}")

