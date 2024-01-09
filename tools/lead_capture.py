import os
import requests
import re
from datetime import datetime

# Environment variable for webhook URL
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # Retrieve your webhook URL from the environment variable.

# Tool configuration
tool_schema = {
    "type": "function",
    "function": {
        "name": "lead_capture",
        "description": "Capture personalized travel information of the lead.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Full name of the user."
                },
                "email": {
                    "type": "string",
                    "description": "Email address of the user."
                },
                "phone_number": {
                    "type": "string",
                    "description": "Phone number of the user."
                },
                "destination_preference": {
                    "type": "string",
                    "description": "Where are you dreaming of going?"
                },
                "travel_style": {
                    "type": "string",
                    "description": "Preference for travel style."
                },
                "pace_of_travel": {
                    "type": "string",
                    "description": "Preference for the pace of travel."
                },
                "trip_focus": {
                    "type": "string",
                    "description": "Main interest or theme for the trip."
                },
                "accommodation_preference": {
                    "type": "string",
                    "description": "Preference for accommodation."
                },
                "travel_companions_age_group": {
                    "type": "string",
                    "description": "Age group of travel companions."
                },
                "trip_duration": {
                    "type": "string",
                    "description": "Duration of the travel adventure."
                },
                "budget_per_person": {
                    "type": "string",
                    "description": "Budget range per person for the journey."
                },
                "preferred_start_date": {
                    "type": "string",
                    "description": "Preferred start date for the travel adventure."
                }
            },
            "required": [
                "name",
                "email",
                "phone_number",
                "destination_preference",
                "travel_style",
                "pace_of_travel",
                "trip_focus",
                "accommodation_preference",
                "travel_companions_age_group",
                "trip_duration",
                "budget_per_person",
                "preferred_start_date"
            ]
        }
    }
}

# Callback function for the 'custom_lead_capture' schema-defined function
def lead_capture(arguments):
    """
    Capture lead's personalized travel details and send the data to a webhook.

    :param arguments: dict, Contains personalized information for capturing lead's travel details.
    :return: dict or str, Response from the webhook or error message.
    """
    # Extracting information from arguments
    name = arguments.get('name')
    email = arguments.get('email')
    phone_number = arguments.get('phone_number')
    destination_preference = arguments.get('destination_preference')
    travel_style = arguments.get('travel_style')
    pace_of_travel = arguments.get('pace_of_travel')
    trip_focus = arguments.get('trip_focus')
    accommodation_preference = arguments.get('accommodation_preference')
    travel_companions_age_group = arguments.get('travel_companions_age_group')
    trip_duration = arguments.get('trip_duration')
    budget_per_person = arguments.get('budget_per_person')
    preferred_start_date = arguments.get('preferred_start_date')

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format. Please provide a valid email address."

    # Prepare data payload for webhook
    data = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "destination_preference": destination_preference,
        "travel_style": travel_style,
        "pace_of_travel": pace_of_travel,
        "trip_focus": trip_focus,
        "accommodation_preference": accommodation_preference,
        "travel_companions_age_group": travel_companions_age_group,
        "trip_duration": trip_duration,
        "budget_per_person": budget_per_person,
        "preferred_start_date": preferred_start_date
    }

    # Send data to webhook
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code in [200, 201]:
            return "Lead capture successful."
        else:
            return f"Error capturing lead details: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Failed to send data to the webhook: {e}"

# Example usage of the 'custom_lead_capture' function:
# lead_info = {
#     'name': 'John Doe',
#     'email': 'john.doe@example.com',
#     'phone_number': '123-456-7890',
#     'destination_preference': 'Paris',
#     'travel_style': 'Private Guided',
#     'pace_of_travel': 'Relaxed',
#     'trip_focus': 'Cultural',
#     'accommodation_preference': 'Luxury - 5 star',
#     'travel_companions_age_group': '36 - 49',
#     'trip_duration': '2 weeks',
#     'budget_per_person': '$5000 - $7000',
#     'preferred_start_date': '2024-05-01'
# }
# lead_capture_response = custom_lead_capture(lead_info)
# print(lead_capture_response)
