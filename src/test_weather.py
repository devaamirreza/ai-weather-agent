from weather_tool import get_weather
import json

# Test our weather function
weather = get_weather("Patna")

# Display the result
print(json.dumps(weather, indent=4))