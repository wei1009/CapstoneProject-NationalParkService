import os
import requests

STATE_PARK_API_URL = "https://developer.nps.gov/api/v1/parks"
GOOGLE_MAP_API_URL ="https://www.google.com/maps/embed/v1/place"

API_SECRET_KEY=os.environ.get('API_SECRET_KEY')
GOOGLE_API_KEY=os.environ.get('Google_API_KEY')

DEFAULT_PARK_API_LIMIT = 1000
DEFAULT_ZOOM_SIZE=13

def get_parks(stateCode, parkCode, limit):

    if limit is None:
        limit = DEFAULT_PARK_API_LIMIT

    if parkCode is None:
        parkCode = ""

    if stateCode is None:
        stateCode=""

    response = requests.get(f"{ STATE_PARK_API_URL }?api_key={ API_SECRET_KEY }&limit={ limit }&parkcode={ parkCode }&statecode={ stateCode}")

    apiParkData = response.json()
    return apiParkData

def get_park_info(apiParkData):

    innerData = apiParkData["data"][0]
    park={"name":innerData["fullName"],
          "states":innerData["states"],
          "parkCode":innerData["parkCode"],
          "mainImage":innerData["images"][0]["url"],
          "images":innerData["images"],
          "email":innerData["contacts"]["emailAddresses"][0]["emailAddress"],
          "city":innerData["addresses"][0]["city"],
          "weatherInfo":innerData["weatherInfo"],
          "description":innerData["description"],
          "url":innerData["url"],
          "activities":innerData["activities"],
          "lat":innerData["latitude"],
          "lng":innerData["longitude"],
          }

    return park

def get_map(coords):
    mapinfo = (f"{ GOOGLE_MAP_API_URL }?key={ GOOGLE_API_KEY }&q={ coords['lat'] },{ coords['lng'] }&zoom={ DEFAULT_ZOOM_SIZE }")
    return mapinfo
