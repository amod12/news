import googlemaps
import wikipedia
from datetime import datetime
import logging

API_KEY = 'AIzaSyBxVti-YamqN4LizQhbZEoQeIYFhe__uZo'

def get_iterinary(places):
    if not places:
        print("from method get_iterinary: places empty!")
        return places
        return []
    places = list(places) # all the middle places
    origin = places[0].ggl_plc_id
    destination = places[-1].ggl_plc_id
    waypoints = []
    through = places[1:-1] # all the middle places
    for place in through:
        waypoints.append("place_id:" + place.ggl_plc_id)
    gmaps = googlemaps.Client(key=API_KEY)
    now = datetime.now()

    try:
        directions_result_drive = gmaps.directions(
            "place_id:" + origin,
            "place_id:" + destination,
            waypoints=waypoints,
            departure_time=now
        )

    except Exception as e:
        return "Error"

    return directions_result_drive


def get_photos_and_text(place_name):
    image_api_link = f"https://maps.googleapis.com/maps/api/place/photo?photoreference=%s&sensor=false&maxheight=1000&maxwidth=1000&key={API_KEY}"
    gclient = googlemaps.Client(key=API_KEY)
    found_place = googlemaps.places.find_place(input=place_name, client=gclient, input_type="textquery")
    target_place_id = found_place['candidates'][0]['place_id']
    # place_detail = googlemaps.places.place(client=gclient, place_id=target_place_id, fields=("photo",))
    # photos_list = []
    # if place_detail["result"]:
    #     photos_list = [image_api_link % photo['photo_reference'] for photo in place_detail['result']['photos']]
    # final_photos = photos_list[:1]
    # try:
    #     text = wikipedia.summary(place_name, sentences=3)
    #     if len(text) > 50:
    #         text = wikipedia.summary(place_name, sentences=2)
    # except wikipedia.exceptions.DisambiguationError as e:
    #     print(e.options)
    # except wikipedia.exceptions.PageError as e:
    #     text = "Data not found"
    final_photos, text = ("", "")
    return final_photos, text

def process_iterinary(places, iterinary_json):
    if not iterinary_json:
        print("from method process_iterinary: iterinary_json empty!")
        return places
    result = {"places": []}
    legs = iterinary_json[0].get('legs')
    legs_length = len(legs) - 1
    for ind, leg in enumerate(legs):
        place_detail = {}
        start_address = leg.get("start_address")
        duration = leg.get("duration")["text"]
        photos, description = get_photos_and_text(start_address)
        place_detail["name"] = start_address
        place_detail["description"] =  description
        place_detail["images"] = photos
        result["places"].append(place_detail)
        result["places"].append({"duration":duration})
        print("---------------")
        print(result)
        print("---------------")
        if ind == legs_length:
            last_place_detail = {}
            end_address = leg.get("end_address")
            photos, description = get_photos_and_text(end_address)
            last_place_detail["name"] = end_address
            last_place_detail["description"] =  description
            last_place_detail["images"] = photos
            result["places"].append(last_place_detail)
            print("+++++++++++++++")
            print(result)
            print("+++++++++++++++")
    return result
