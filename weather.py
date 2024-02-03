import requests

# Set the API endpoint URL
url = "https://weatherapi-com.p.rapidapi.com/current.json"


def get_weather(city) -> str:
    """
    Get the current weather information for a given city.

    Args:
        city (str): The name of the city.

    Returns:
        str: The weather information in a formatted string.
    """
    # Set the query parameters
    querystring = {'q': city}

    # Set the headers for the API request
    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "f8c37bfbb9mshe2a8ff4fe61e343p17e654jsn13cbf18d0f45",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    # Make the API request
    response = requests.get(url, headers=headers, params=querystring)

    # Parse the response data
    data = response.json()

    # Format the weather information
    result = (f"Текущая погода в городе {data['location']['name']} \n"
              f", {data['location']['country']} \n" \
              f"Температура воздуха : {data['current']['temp_c']} C\n" \
              f"Влажность воздуха : {data['current']['humidity']}\n" \
              f"Ощущается как : {data['current']['feelslike_c']}\n" \
              f"Облачность : {data['current']['cloud']}\n" \
              f"UV индекс : {data['current']['uv']}")

    return result

# response = b'{"location":{"name":"Riga","region":"Riga","country":"Latvia","lat":56.95,"lon":24.1,' \
#          b'"tz_id":"Europe/Riga",' \
#     b'"localtime_epoch":1706444259,"localtime":"2024-01-28 14:17"},"current":{"last_updated_epoch":1706444100,' \
#     b'"last_updated":"2024-01-28 14:15","temp_c":2.0,"temp_f":35.6,"is_day":1,"condition":{"text":"Overcast",' \
#     b'"icon":"//cdn.weatherapi.com/weather/64x64/day/122.png","code":1009},"wind_mph":5.6,"wind_kph":9.0,' \
#     b'"wind_degree":200,"wind_dir":"SSW","pressure_mb":1030.0,"pressure_in":30.42,"precip_mm":0.0,"precip_in":0.0,' \
#     b'"humidity":93,"cloud":100,"feelslike_c":-0.9,"feelslike_f":30.5,"vis_km":10.0,"vis_miles":6.0,"uv":1.0,' \
#     b'"gust_mph":11.6,"gust_kph":18.6}}'
