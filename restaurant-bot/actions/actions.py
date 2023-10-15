
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from typing import Text, List, Dict, Any
from . import LOCATIONS, RESTANRANTS, ORDER_MANAGER

import datetime
import uuid


class ActionSearchRestaurant(Action):
    def name(self) -> Text:
        return "action_find_restaurant"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            location = tracker.get_slot("location")
            log_time = datetime.datetime.now()
            log_time_str = log_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{log_time_str}||action_find_restaurant||location:{location}")
            if location == None:
                error_message = "Excuse me, where would you like to go to a restaurant near here?"
                dispatcher.utter_message(error_message)
                return []

            # Find restaurant information based on the location provided by the user
            if location in LOCATIONS:
                # print(f"Location: {location}")
                # print("Restaurants:")
                # for restaurant, info in RESTANRANTS.items():
                #     print(restaurant, info["location"])
                nearby_restaurants = [restaurant for restaurant, info in RESTANRANTS.items(
                ) if info["location"] == location]
                if nearby_restaurants:
                    restaurant_list = "\n".join(nearby_restaurants)
                    response_message = f"Here are some nearby restaurants: \n{restaurant_list}"
                else:
                    response_message = "No restaurants nearby"
            else:
                response_message = "Sorry, the location you provided could not be found."
            
            dispatcher.utter_message(response_message)
        except Exception as _:
            error_message = "Sorry, there are some problems, please try again later."
            dispatcher.utter_message(error_message)
        return []

class ActionBrowseMenu(Action):
    def name(self) -> Text:
        return "action_view_menu"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            restaurant = tracker.get_slot("restaurant")
            if restaurant == None:
                error_message = "Excuse me, which restaurant would you like to have dinner at?"
                dispatcher.utter_message(error_message)
                return []
            if restaurant in RESTANRANTS:
                memu = RESTANRANTS[restaurant]["menu"]
                if memu:
                    memu_list = "\n".join(memu)
                response_message = f"Here is the menu for {restaurant}:\n{memu_list}"
            else:
                response_message = "Sorry, the restaurant you provided cannot be found."
            
            dispatcher.utter_message(response_message)
        except Exception as _:
            error_message = "Sorry, there are some problems, please try again later."
            dispatcher.utter_message(error_message)
        return []

class ActionOrderDish(Action):
    def name(self) -> Text:
        return "action_order_dish"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            dish = tracker.get_slot("dish")
            restaurant = tracker.get_slot("restaurant")
            log_time = datetime.datetime.now()
            log_time_str = log_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{log_time_str}||action_order_dish||restaurant:{restaurant}||dish:{dish}")
            if restaurant is None:
                error_message = "Excuse me, where are you near?"
                dispatcher.utter_message(error_message)
                return []
            if dish is None:
                error_message = "Excuse me, what kind of food would you like to have?"
                dispatcher.utter_message(error_message)
                return []
            if restaurant in RESTANRANTS:
                memu = RESTANRANTS[restaurant]["menu"]
                if dish in memu:
                    # order_id = uuid.uuid4()
                    # bytes_uuid = order_id.bytes
                    
                    # hex_uuid = ''.join('{:02x}'.format(b) for b in bytes_uuid)

                    # order_id_str = str(hex_uuid)

                    current_datetime = datetime.datetime.now()
                    #Converts a datetime object to a string
                    date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    id = ORDER_MANAGER.create_order(dish, date_time_str)
                    if id is None:         
                        error_message = "Sorry, there are some problems, please try again later."
                        dispatcher.utter_message(error_message)
                        return []
                    else: 
                        response_message = f"You ordered a {dish} from {date_time_str} at {restaurant}, please pick up your order number: {id}."
                else:
                    response_message = "Sorry, it's not on the menu."
            else:
                response_message = "Sorry, the restaurant you provided cannot be found."

            dispatcher.utter_message(response_message)
        except Exception as _:
            error_message = "Sorry, there are some problems, please try again later."
            dispatcher.utter_message(error_message)
        return []

class ActionCancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            # Cancellation logic
            # The user's order can be found in the database and cancelled
            oid = tracker.get_slot("oid")
            log_time = datetime.datetime.now()
            log_time_str = log_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{log_time_str}||action_cancel_order||order_id:{oid}")
            if oid == None:
                error_message = "Excuse me, which order would you like to cancel?"
                dispatcher.utter_message(error_message)
                return []
            status = ORDER_MANAGER.delete_order(oid)
            if status == "success":
                response_message = f"Your order: {oid} cancelled."
            else:
                response_message = "Sorry, this order cannot be found. Sorry, this order cannot be found."
            dispatcher.utter_message(response_message)
        except Exception as _:
            error_message = "Sorry, there are some problems, please try again later."
            dispatcher.utter_message(error_message)
        return []

class ActionTrackOrder(Action):
    def name(self) -> Text:
        return "action_track_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            
            oid = tracker.get_slot("oid")
            log_time = datetime.datetime.now()
            log_time_str = log_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{log_time_str}||action_track_order||order_id:{oid}")
            if oid == None:
                error_message = "Excuse me, which order would you like to inquire about?"
                dispatcher.utter_message(error_message)
                return []
            current_datetime = datetime.datetime.now()
            date_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            status = ORDER_MANAGER.get_order_status(oid, date_time_str)
            if status is None:
                response_message = "Sorry, this order cannot be found."
            else:
                response_message = f"The status of your order is:{status}."
            dispatcher.utter_message(response_message)
        except Exception as _:
            error_message = "Sorry, there are some problems, please try again later."
            dispatcher.utter_message(error_message)
        return []
