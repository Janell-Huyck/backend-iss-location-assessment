#!/usr/bin/env python3
#


import sys
import requests
import turtle
import time


__author__ = "Janell.Huyck"

if sys.version_info[0] < 3:
    raise Exception("This program requires python3 interpreter")


astros_api = 'http://api.open-notify.org/astros.json'
iss_position_api = 'http://api.open-notify.org/iss-now.json'
indy_location_dict = {"longitude": -86.148003, "latitude": 39.791000}

indy_coordinates = (indy_location_dict["longitude"],
                    indy_location_dict["latitude"])

with open("poem.txt") as f:
    poem = f.read()


def get_astronaut_stats():
    """ Prints names of astronauts, their crafts,
    and total # of astronauts"""

    r = requests.get(astros_api).json()
    number_astros = r['number']
    people = r['people']
    for astro in people:
        astro_name = astro['name']
        astro_craft = astro['craft']
        print(f'Astronaut: {astro_name} \tCraft: {astro_craft}')
    print("Total number of Astronauts: ", number_astros)
    return r


def get_iss_stats():
    """ Returns the longitude, latitude, and timestamp for the
    current location of the ISS"""

    r = requests.get(iss_position_api).json()
    longitude = r['iss_position']['longitude']
    latitude = r['iss_position']['latitude']
    timestamp = r['timestamp']
    return longitude, latitude, timestamp


def get_next_pass_time():
    """Returns the next pass time for the ISS over
    Indianapolis, IN."""

    location = indy_coordinates  # longitude, latitude
    lon = location[0]
    lat = location[1]

    # returns information about next pass time.
    r = requests.get(
        f'http://api.open-notify.org/iss-pass.json?lat={lat}&lon={lon}&n=1')
    r = r.json()
    risetime = r['response'][0]['risetime']

    return risetime


def trace_iss_path():
    """ Draws map, ISS, Indianapolis, and timestamp"""

    print("Click anywhere on the map to close the screen...")

    risetime = get_next_pass_time()
    risetime = time.ctime(risetime)

    # set up the turtle screen
    screen = turtle.Screen()
    screen.setup(width=720, height=360)
    screen.addshape("iss.gif")
    screen.bgpic("map.gif")
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.screensize(canvwidth=500, canvheight=200)

    # space_station graphically shows where the ISS is
    space_station = turtle.Turtle()
    space_station.shape('iss.gif')
    space_station.penup()

    # indy_pin shows were Indianapolis,IN is and next pass time
    indy_pin = turtle.Turtle()
    indy_pin.penup()
    indy_pin.hideturtle()
    indy_pin.goto(indy_coordinates)
    indy_pin.dot(10, 'yellow')
    indy_pin.color('white')
    indy_pin.write("Next pass: \n" + str(risetime) +
                   '\n Kenzietown, IN')

    # station_clock displays the time for the ISS location data
    station_clock = turtle.Turtle()
    station_clock.penup()
    station_clock.hideturtle()
    station_clock.goto(-10, -90)
    station_clock.color('black')
    station_clock.write("Loading...")

    def outtahere(*args):
        """Closes the turtle when the screen is clicked.
        Using this instead of screen.exitonclick() because
        that freezes the program and won't let the while
        loop execute."""

        turtle.bye()

    # When screen is clicked, close the turtle
    screen.onclick(outtahere)

    # Every second, update ISS position and timestamp
    while True:
        try:
            longitude, latitude, timestamp = get_iss_stats()
            timestamp = time.ctime(timestamp)
            space_station.goto(float(longitude), float(latitude))
            station_clock.clear()
            station_clock.write("Time of ISS stats: " +
                                timestamp, False, align='left',
                                font=('Arial', 12, 'bold'))
            time.sleep(1)

        # Exception happens when turtle.bye() has executed.
        except Exception:
            sys.exit(poem)


def main():
    get_astronaut_stats()
    trace_iss_path()


if __name__ == '__main__':
    main()
