import requests
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Function to fetch data from the Squiggle API
def fetch_squiggle_data():
    url = "https://api.squiggle.com.au/sse/test"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from Squiggle API.")
        return None

# Initialize RGB matrix
options = RGBMatrixOptions()
# Configure RGB matrix options as needed
matrix = RGBMatrix(options=options)

# Fetch data from Squiggle API
squiggle_data = fetch_squiggle_data()

# Display fetched data on RGB matrix (example)
if squiggle_data:
    # Example: Display fetched data on the RGB matrix
    for row in squiggle_data:
        for pixel in row:
            # Example: Set pixel color based on fetched data
            # Replace with actual logic to map data to RGB colors
            r, g, b = pixel['r'], pixel['g'], pixel['b']
            # Example: Display pixel color on the RGB matrix
            matrix.SetPixel(pixel['x'], pixel['y'], r, g, b)

# Optionally add more code for processing and displaying the data on the matrix

