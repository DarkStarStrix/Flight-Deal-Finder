import requests
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

# 1. Update the IATA Codes
# 2. Use the FlightSearch class to check for deals
# 3. If there is a flight that is under £300, use the NotificationManager to send an SMS to your own number
# 4. The message should include the departure airport IATA code, destination airport IATA code, departure city, destination city, flight price and flight dates.

ORIGIN_CITY_IATA = "LON"

connection = requests.get(url="https://api.sheety.co/0b9b0b0c6b0b0b0b0b0b0b0b0b0b0b0b/flightDeals/prices")
print(connection.status_code)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()

notification_manager = NotificationManager()

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )
