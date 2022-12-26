import requests
import json

# Set the API endpoint and parameters
endpoint = "https://api.nasa.gov/planetary/earth/assets?api_key=B55H5anQGne0BiseUvFPPp6XQFKkummCeWRxIo8S"
params = {
    'lat': 47.61,  # Latitude of the area you want to take a picture of
    'lon': -122.34,  # Longitude of the area you want to take a picture of
    'dim': 0.001,  # Image size in degrees, 0.001 is roughly 1 km
    'date': '2022-06-01',  # Date of the image
}

# Send the GET request to the API

response = requests.get(endpoint, params=params)
print(response)
# Check if the request was successful
if response.status_code == 200:
    # Parse the response as JSON
    data = json.loads(response.text)

    # Extract the URL of the image
    image_url = data['url']

    # Download the image
    image_response = requests.get(image_url)

    # Check if the download was successful
    if image_response.status_code == 200:
        # Save the image to a file
        with open('image.jpg', 'wb') as f:
            f.write(image_response.content)
        print('Image saved to file')
    else:
        print('Failed to download image')
else:
    print('Failed to request image')
