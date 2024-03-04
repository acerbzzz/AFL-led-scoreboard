import json
from datetime import datetime
from rgbmatrix import RGBMatrix, graphics
import time

# JSON data provided by the user
json_data = '''
<  "$ref": "http://sports.core.api.espn.com/v2/sports/australian-football/leagues/afl?lang=en&region=us",
  "id": "35",
  "guid": "87d86d88-cd6d-3e32-a712-2a9f6c5d48cf",
  "uid": "s:34~l:35",
  "name": "AFL",
  "displayName": "AFL",
  "abbreviation": "AFL",
  "shortName": "AFL",
  "midsizeName": "AFL",
  "slug": "afl",
  "isTournament": false,
  "season": {
    "$ref": "http://sports.core.api.espn.com/v2/sports/australian-football/leagues/afl/seasons/2024?lang=en&region=us",
    "year": 2024,
    "startDate": "2024-02-21T08:00Z",
    "endDate": "2024-10-02T06:59Z",
    "displayName": "2024",
    "type": {
      "$ref": "http://sports.core.api.espn.com/v2/sports/australian-football/leagues/afl/seasons/2024/types/1?lang=en&region=us",
      "id": "1",
      "type": 1,
      "name": "Preseason",
      "abbreviation": "pre",
      "year": 2024,
      "startDate": "2024-02-21T08:00Z",
      ">
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
