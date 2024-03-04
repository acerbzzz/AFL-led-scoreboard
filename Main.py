import json
from datetime import datetime
from rgbmatrix import RGBMatrix, graphics
import time

# Insert your JSON data here
json_data = '''
{
  "events": [
    {
      "date": "2024-03-03T08:00:00Z",
      "teams": [
        {"displayName": "Team A"},
        {"displayName": "Team B"}
      ]
    },
    {
      "date": "2024-03-04T10:00:00Z",
      "teams": [
        {"displayName": "Team C"},
        {"displayName": "Team D"}
      ]
    }
  ]
}
'''

# Load JSON data
data = json.loads(json_data)

# Extract information about live and upcoming games
live_games = []
upcoming_games = []

# Navigate to the relevant sections containing information about games
games = data.get('events', [])

for game in games:
    # Extract game details
    game_date = datetime.strptime(game.get('date'), '%Y-%m-%dT%H:%M:%SZ')
    teams = game.get('teams', [])
    team1 = teams[0].get('displayName')
    team2 = teams[1].get('displayName')
    
    # Determine if the game is live or upcoming
    current_time = datetime.now()
    if game_date < current_time:
        live_games.append({'team1': team1, 'team2': team2})
    else:
        upcoming_games.append({'team1': team1, 'team2': team2, 'date': game_date})

# Initialize LED matrix
matrix = RGBMatrix(32, 32, 2)

# Load font
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/5x8.bdf")

# Define colors
COLOR_RED = graphics.Color(255, 0, 0)
COLOR_GREEN = graphics.Color(0, 255, 0)

# Display live games and upcoming games with scrolling text
def display_games(matrix, games, color):
    text = ""
    for game in games:
        text += f"{game['team1']} vs {game['team2']}    "
    len_text = graphics.TextWidth(font, text)
    offscreen_canvas = matrix.CreateFrameCanvas()
    pos = offscreen_canvas.width
    while True:
        offscreen_canvas.Clear()
        len_text = graphics.DrawText(offscreen_canvas, font, pos, 8, color, text)
        pos -= 1
        if pos + len_text < 0:
            pos = offscreen_canvas.width
        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
        time.sleep(0.05)

# Display live games with scrolling text in red
display_games(matrix, live_games, COLOR_RED)

# Display upcoming games with scrolling text in green
display_games(matrix, upcoming_games, COLOR_GREEN)
