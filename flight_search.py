from datetime import datetime, timedelta

import requests

from flight_data import FlightData


def get_kiwi_api_headers():
    with open("kiwi_api_key.txt") as file:
        return {
            "apikey": file.read()
        }


class FlightSearch:
    def __init__(self, kiwi_api_headers=None):
        self.connection = requests.get(url="https://tequila-api.kiwi.com/locations/query", headers=kiwi_api_headers)
        self.data = self.connection.json()
        self.iata_codes = {row["code"]: row["id"] for row in self.data["locations"]}
        self.date_from = datetime.now().strftime("%d/%m/%Y")
        self.date_to = (datetime.now() + timedelta(days=180)).strftime("%d/%m/%Y")

    def get_destination_code(self, city_name):
        return self.iata_codes[city_name]

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        request = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }

        connection = requests.get(
            url="https://tequila-api.kiwi.com/v2/search",
            params=request,
            headers=self.connection.headers
        )

        try:
            data = connection.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )

        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data
