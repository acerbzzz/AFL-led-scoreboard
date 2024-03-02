import requests
import json
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

def fetch_squiggle_data(endpoint):
    url = f"https://api.squiggle.com.au/sse/{endpoint}"
    response = requests.get(url)
    data = response.json()
    return data

def format_game_info(game):
    game_info = f"{game['hteam']} vs {game['ateam']}\n"
    game_info += f"Venue: {game['venue']}\n"
    game_info += f"Date: {game['date']}\n"
    game_info += f"Time: {game['timestr']}"
    return game_info

def display_on_led_matrix(game_info, matrix):
    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("../../../fonts/5x8.bdf")
    textColor = graphics.Color(255, 255, 255)
    pos = 1
    graphics.DrawText(canvas, font, pos, 10, textColor, game_info)
    canvas = matrix.SwapOnVSync(canvas)

def display_games(games, matrix):
    for game in games:
        game_info = format_game_info(game)
        display_on_led_matrix(game_info, matrix)
        time.sleep(5)  # Display each game for 5 seconds

def main():
    # Initialize LED matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    matrix = RGBMatrix(options=options)

    try:
        # Fetch live and upcoming games
        live_games = fetch_squiggle_data("games")
        upcoming_games = fetch_squiggle_data("events")

        # Display live games
        display_games(live_games, matrix)

        # Display upcoming games
        display_games(upcoming_games, matrix)

    except KeyboardInterrupt:
        matrix.Clear()

if __name__ == "__main__":
    main()

