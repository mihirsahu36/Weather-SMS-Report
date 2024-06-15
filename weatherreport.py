from pyowm import OWM
from pyowm.utils.config import get_default_config
from twilio.rest import Client
from credentials import my_twilio_number, account_sid, auth_token, my_phone_number, owm_api_key

owm = OWM(owm_api_key)
mgr = owm.weather_manager()

def umbrellaNotRequired(weather):
    """
    Function to determine if an umbrella is not required based on weather conditions.
    """
    rain = weather.rain
    status = weather.status.lower().strip()

    # Check if there's no rain or the weather is clear
    if not rain or status == "clear":
        return True
    return False

def send_weather_sms():
    """
    Function to send weather update SMS.
    """
    try:
        # Fetch weather for Bangalore
        observation = mgr.weather_at_place('Bangalore,IN')
        weather = observation.weather

        if observation:
            # Check if umbrella is not required
            if umbrellaNotRequired(weather):
                temperature = weather.temperature('celsius')['temp']
                humidity = weather.humidity

                client = Client(account_sid, auth_token)

                # Send SMS
                message = f"Hey, sky is clear and you don't need an umbrella. Weather details:\n1. Humidity: {humidity}%\n2. Temperature: {temperature} Celsius"
                client.messages.create(from_=my_twilio_number, to=my_phone_number, body=message)
            else:
                print("Umbrella required. No SMS sent.")
        else:
            print("OWM API returned no data. No SMS sent.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        # Handle exceptions, e.g., log the error

if __name__ == '__main__':
    send_weather_sms()
