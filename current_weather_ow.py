#!/usr/bin/python3

from datetime import datetime
import time
from os.path import exists
import json
import requests

# User Settings
latitude = 39.759444    # replace with your local latitude
longitude = -84.191667  # replace with your local longitude
api_key = 'replace-with-your-openweather-api-key'

degree_sign = u'\N{DEGREE SIGN}'
rounding_precision = 0  # decimal places
config_file = 'current_weather_ow.json'

def get_current_weather():
	'''
	Call the OpenWeather API and request the current weather conditions.
	'''
	url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}'
	response = requests.get(url)

	return response

def convert_temperature(temp_k):
	'''
	Input format:  Kelvin

	Output format: Fahrenheit
	'''
	temp_f = temp_k * 9/5 - 459.67

	return round(temp_f, rounding_precision)

def convert_windspeed(windspeed_ms):
	'''
	Input format:  meters/sec

	Output format: miles/hour
	'''
	meters_per_hour = windspeed_ms * 60 * 60
	miles_per_hour = meters_per_hour * 1 / 1609.344

	return round(miles_per_hour, rounding_precision)

def get_cardinal_direction(degrees):
	'''
	Given a cardinal direction in degrees, this will return a friendly direction description,
	e.g., 'E' for 90 degrees.
	'''
	dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
	ix = int((degrees + 11.25)/22.5)

	return dirs[ix % 16]

def get_min_max_temp(current_temp):
	'''
	Track minimum and maximum temperatures for the day.
	'''
	current_time = datetime.now().strftime("%H:%M")
	min_temp,max_temp = -99,-99
	min_time,max_time = current_time,current_time

	if exists(config_file):
		with open(config_file, "r") as config_stream:
			config_data = json.load(config_stream)
			tracking_day = datetime.strptime(config_data["tracking_day"], "%Y-%m-%d")
			current_day = datetime.today()
			if tracking_day.date() != current_day.date():
				tracking_day = current_day.date()
				min_temp = current_temp
				max_temp = current_temp
			else:
				tracking_day = tracking_day.date()
				min_temp = config_data["min_temp"]
				max_temp = config_data["max_temp"]
				if "min_time" in config_data:
					min_time = config_data["min_time"]
				if "max_time" in config_data:
					max_time = config_data["max_time"]
				if current_temp < min_temp:
					min_temp = current_temp
					min_time = current_time
				if current_temp > max_temp:
					max_temp = current_temp
					max_time = current_time

		output_dict = { }
		output_dict["tracking_day"] = str(tracking_day)
		output_dict["min_temp"] = min_temp
		output_dict["max_temp"] = max_temp
		output_dict["min_time"] = min_time
		output_dict["max_time"] = max_time

		with open(config_file, "w") as config_stream:
			json.dump(output_dict, config_stream, indent=4)

	return (round(min_temp,rounding_precision),round(max_temp,rounding_precision),time.strftime("%I:%M %p", strtotime(min_time)),time.strftime("%I:%M %p", strtotime(max_time)))

def strtotime(time_string):
    date_var = time.strptime(time_string, '%H:%M')

    return date_var

def get_sunrise_sunset(result):
	'''
	Convert sunrise and sunset times from UNIX UTC to friendly strings, e.g., '07:42 AM' and '06:02 PM'
	'''
	sunrise_utc = result["sys"]["sunrise"]
	sunset_utc = result["sys"]["sunset"]
	timezone_offset = result["timezone"]

	sunrise_value = datetime.utcfromtimestamp(sunrise_utc + timezone_offset)
	sunset_value = datetime.utcfromtimestamp(sunset_utc + timezone_offset)

	sunrise_str = str(sunrise_value.time().strftime("%I:%M %p"))
	sunset_str = str(sunset_value.time().strftime("%I:%M %p"))

	return (sunrise_str,sunset_str)

if __name__ == "__main__":
	result = json.loads(get_current_weather().text)

	location = result["name"]
	description = result["weather"][0]['description']
	cloud_percent = result["clouds"]["all"]
	actual_temperature = convert_temperature(result["main"]["temp"])
	feels_like_temperature = convert_temperature(result["main"]["feels_like"])
	wind_speed = convert_windspeed(result["wind"]["speed"])
	try:
		wind_speed_gust = convert_windspeed(result["wind"]["gust"])
	except:
		wind_speed_gust = 0
	wind_cardinal = get_cardinal_direction(result["wind"]["deg"])
	min_temp,max_temp,min_time,max_time = get_min_max_temp(actual_temperature)

	(sunrise_str,sunset_str) = get_sunrise_sunset(result)

	print(location)
	print(f"  {int(actual_temperature)}{degree_sign} (feels like {int(feels_like_temperature)}{degree_sign})")
	print(f"  {description}, {cloud_percent}% cloud cover")
	print(f"  -----")
	#print(f"wind: {wind_cardinal} at {int(wind_speed)} MPH (gusting to {int(wind_speed_gust)})")
	if min_temp != -99:
		print(f"  min: {int(min_temp)}{degree_sign} at {min_time}")
		print(f"  max: {int(max_temp)}{degree_sign} at {max_time}")
		print(f"  -----")
	print(f"  sunrise: {sunrise_str}")
	print(f"  sunset: {sunset_str}")
	
