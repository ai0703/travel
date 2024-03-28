import os
import requests
import re
from datetime import datetime




# Tool configuration
tool_config = {
    "type": "function",
    "function": {
        "name": "get_flight_prices",
        "description": "Retrieves flight details and prices for specified departure and destination cities, along with the departure date.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_city": {
                    "type": "string",
                    "description": "The departure city."
                },
                "to_city": {
                    "type": "string",
                    "description": "The destination city."
                },
                "depart_date": {
                    "type": "string",
                    "description": "The departure date in YYYY-MM-DD format."
                },
                "currency_code": {
                    "type": "string",
                    "description": "The currency code for the price retrieval (default: AED).",
                    "default": "AED"
                }
            },
            "required": ["from_city", "to_city", "depart_date"]
        }
    }
}

# The callback function (Retrieves flight prices and details)
def get_flight_prices(arguments):
    """
    Retrieves the minimum flight prices for a given route and departure date.

    :param arguments: dict, Contains information about the route and date.
                      Expected keys: from_city, to_city, depart_date, (optional) currency_code.
    :return: dict or str, Flight price details in JSON format or error message.
    """
    from_city = arguments.get('from_city')
    to_city = arguments.get('to_city')
    depart_date = arguments.get('depart_date')
    currency_code = arguments.get('currency_code', 'AED')  # Default currency code AED

    # Function to fetch airport ID based on city name
    def get_airport_id(city):
        url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination"
        querystring = {"query": city}
        headers = {
            "X-RapidAPI-Key": "334656b9fcmsh7165acee3c3fd38p1aaa3ejsnb0d029f2d419",
            "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            if data and 'data' in data and len(data['data']) > 0:
                airport_id = data['data'][0]['id']
                return airport_id
            else:
                return None
        else:
            return None

    # Function to retrieve flight prices
    from_airport_id = get_airport_id(from_city)
    to_airport_id = get_airport_id(to_city)

    if not from_airport_id or not to_airport_id:
        return "Unable to fetch airport IDs. Please check city names and try again."

    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/getMinPrice"
    querystring = {
        "fromId": from_airport_id,
        "toId": to_airport_id,
        "departDate": depart_date,
        "currency_code": currency_code
    }
    headers = {
        "X-RapidAPI-Key": "334656b9fcmsh7165acee3c3fd38p1aaa3ejsnb0d029f2d419",
        "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return "Failed to retrieve flight prices. Status code: {}".format(response.status_code)

