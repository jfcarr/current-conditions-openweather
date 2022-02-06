# current-conditions-openweather

Simple text output of current weather conditions, retrieved from OpenWeather API.  (I use the output in a [Conky](https://github.com/brndnmtthws/conky) configuration)

Before using the script, you'll need to sign up for access to the [OpenWeather API](https://openweathermap.org/api).  I use the free tier, which provides more than enough calls-per-month for personal use.  Once you've signed up, you'll be assigned an API key you can use in the script.

Sample output:

```
Dayton
  18° (feels like 8°)
  clear sky, 0% cloud cover
  -----
  today's min,max: 18°,23°
  sun rise,set: 07:40 AM,06:00 PM
```

## Daily Temperature Minimum and Maximum

If you're running the script regularly, and you want to track daily high and low temperatures, create a `current_weather_ow.json` file in the script's working directory, with the following contents:

```json
{
    "tracking_day": "1980-01-01",
    "min_temp": -99,
    "max_temp": -99
}
```

Each time the script runs, it will compare the current date and temperature to the values in the .json file, and update them accordingly.  At midnight, the tracking values will be reset.

## Measurements

These are the default measurements in returned values.  Information comes from [here](https://openweathermap.org/current).

Value | Measurement
---------|----------
Temperature | Kelvin
Humidity | Percentage
Wind Speed | Meters/second
Time of Date Calculation (dt) | UTC, UNIX format

The script automatically converts these to Imperial values.
