#!/usr/bin/env python

from sodapy import Socrata
import datetime
import sys
import os

SOCRATA_DOMAIN = "data.sfgov.org"
FOOD_TRUCKS_RESOURCE_IDENTIFIER = "bbb8-hzi6"
LIMIT = 10
SOCRATA_TOKEN = os.environ.get("SODAPY_APPTOKEN")


def get_current_time_string():
    """
    get current time in format HH:MM

    :return: string
    """
    return datetime.datetime.now().strftime('%H:%M')


def get_current_day_index():
    """
    get current day in int representation

    :return: int
    """
    return datetime.date.today().weekday()


def get_query_string(weekday_index, current_time_string):
    """
    Constructs SOQL query string to get food trucks open at current time and day
    For more information: https://dev.socrata.com/docs/queries/

    :param weekday_index: string
    :param current_time_string: string
    :return: string
    """
    # query if time is between start and end time if start and end time are on same day (ie. 7/21 10am-7pm)
    query_time_same_day = "(dayorder = %s and start24<end24 and \"%s\" < end24 and \"%s\" > start24)" % (
        weekday_index, current_time_string, current_time_string
    )
    # query if current time is in hours overflowed from the previous day (ie. from 7/21 9pm until 7/22 3am)
    query_time_overflow_day = "(dayorder = %s and end24<start24 and (\"%s\"< end24 or \"%s\" >start24))" % (
        weekday_index-1, current_time_string, current_time_string
    )
    return query_time_same_day + " or " + query_time_overflow_day


def get_food_trucks(page_number):
    """
    Gets list of food trucks in array representation from Socrata client

    :param page_number: int
    :return: array representation of food trucks
    """
    weekday_index = get_current_day_index()
    current_time_string = get_current_time_string()
    client = Socrata(SOCRATA_DOMAIN, SOCRATA_TOKEN)
    food_trucks = client.get(FOOD_TRUCKS_RESOURCE_IDENTIFIER,
                             select="applicant, location",
                             where=get_query_string(weekday_index, current_time_string),
                             limit=LIMIT,
                             offset=page_number * LIMIT,
                             order="applicant ASC")
    return food_trucks


def print_food_trucks(food_trucks):
    """
    Prints name and location of food trucks with in line column formatting

    :param food_trucks: array
    :return: void
    """
    print('{0:<60} {1:<30}'.format('Name', 'Location'))
    for food_truck in food_trucks:
        name = food_truck['applicant']
        location = food_truck['location']
        print('{0:<60} {1:<30}'.format(name, location))


def main():
    page_number = 0
    while True:
        food_trucks = get_food_trucks(page_number)
        if food_trucks:
            print_food_trucks(food_trucks)
        else:
            sys.stdout.write("No Food Trucks found")

        # no further results available
        if len(food_trucks) < LIMIT:
            return

        sys.stdout.write("Show more results [Y/N]: ")
        choice = input().lower()
        if choice == 'y':
            page_number += 1
        else:
            return


if __name__ == "__main__":
    main()
