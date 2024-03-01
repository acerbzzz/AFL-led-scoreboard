import requests
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import json

# Define the URL for the Event API
event_api_url = "https://api.squiggle.com.au/sse/events"

# Initialize the RGB matrix options
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "regular"

# Initialize the RGB matrix
matrix = RGBMatrix(options = options)

# Function to parse and display game events on the LED matrix
def display_game_events():
    try:
        # Connect to the Event API
        response = requests.get(event_api_url, stream=True)
        
        # Loop through the stream of events
        for line in response.iter_lines():
            if line:
                # Parse the JSON data
                event_data = json.loads(line)
                
                # Extract relevant information from the event
                game_id = event_data.get("data", {}).get("id")
                team_scores = event_data.get("data", {}).get("score", {})
                
                # Format the scores for display
                score_text = f"Home: {team_scores.get('hscore')} - Away: {team_scores.get('ascore')}"
                
                # Display the scores on the LED matrix
                matrix.Clear()
                matrix.DrawText(0, 16, matrix.Color(255, 255, 255), score_text)
                
    except Exception as e:
        print("Error:", e)
        # Handle disconnection and auto-reconnection here if needed

# Call the function to start displaying game events
display_game_events()
