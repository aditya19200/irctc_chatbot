import datetime
import time

# --- Placeholder Data (Replace with API calls in a real application) ---

# Simulated train data: { "ORIGIN-DEST": { "DD-MM-YYYY": [ {train_details...}, ... ] } }
train_data = {
    "SBC-MAS": { # KSR Bengaluru (SBC) to Chennai Central (MAS)
        "25-12-2025": [
            {"no": "12008", "name": "SHATABDI EXP", "dep": "06:00", "arr": "11:00",
             "classes": {"CC": {"avail": "AVL 50", "fare": 650}, "EC": {"avail": "AVL 10", "fare": 1250}}},
            {"no": "22626", "name": "DOUBLE DECKER", "dep": "14:30", "arr": "20:30",
             "classes": {"CC": {"avail": "AVL 120", "fare": 580}}},
            {"no": "12658", "name": "CHENNAI MAIL", "dep": "22:40", "arr": "04:25",
             "classes": {"SL": {"avail": "AVL 200", "fare": 350}, "3A": {"avail": "WL 10/WL 5", "fare": 950},
                         "2A": {"avail": "AVL 15", "fare": 1350}, "1A": {"avail": "AVL 5", "fare": 2250}}}
        ],
         "26-12-2025": [
            # ... add data for other dates if needed
         ]
    },
    "NDLS-MMCT": { # New Delhi (NDLS) to Mumbai Central (MMCT)
         "25-12-2025": [
             {"no": "12952", "name": "MUMBAI RAJDHANI", "dep": "16:55", "arr": "08:35",
             "classes": {"3A": {"avail": "AVL 80", "fare": 2100}, "2A": {"avail": "AVL 40", "fare": 3000}, "1A": {"avail": "AVL 12", "fare": 5100}}}
         ]
    }
    # Add more routes as needed
}

# Simulated nearby stations: { "STATION_CODE": [List of nearby stations] }
nearby_stations_data = {
    "SBC": ["Bengaluru Cantt. (BNC)", "Yesvantpur Jn (YPR)", "Krishnarajapuram (KJM)"],
    "MAS": ["Chennai Egmore (MS)", "Tambaram (TBM)", "Perambur (PER)"],
    "NDLS": ["Old Delhi Jn (DLI)", "Hazrat Nizamuddin (NZM)", "Anand Vihar Terminal (ANVT)"],
    "MMCT": ["Dadar (DR)", "Bandra Terminus (BDTS)", "Lokmanya Tilak Terminus (LTT)"]
}

# --- Chatbot Functions ---

def bot_print(message):
    """Prints bot messages with a slight delay"""
    print(f"Bot: {message}")
    time.sleep(0.5) # Simulate typing/processing delay

def get_valid_input(prompt, validation_func=None, error_message="Invalid input."):
    """Gets input and optionally validates it."""
    while True:
        user_input = input(f"You: ").strip()
        if validation_func:
            if validation_func(user_input):
                return user_input
            else:
                bot_print(error_message)
                bot_print(prompt) # Repeat the prompt
        elif user_input: # Basic check for non-empty input if no validation function
             return user_input
        else:
             bot_print("Input cannot be empty. " + prompt)


def validate_station_code(code):
    # Basic check - could be more complex (e.g., check against a list)
    return len(code) >= 3 and code.isupper()

def validate_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%d-%m-%Y')
        # Could add check if date is in the past, but skipping for simplicity
        return True
    except ValueError:
        return False

def validate_yes_no(answer):
    return answer.lower() in ['yes', 'y', 'no', 'n']

def validate_integer(num_str):
    return num_str.isdigit()

# --- Main Chat Flow ---

def run_chatbot():
    bot_print("Welcome to the IRCTC booking assistant! 👋")
    bot_print("Would you like me to help you find and book a train ticket today? (yes/no)")
    start_search = get_valid_input("Please answer 'yes' or 'no'.", validate_yes_no)

    if start_search.lower() not in ['yes', 'y']:
        bot_print("Okay, let me know if you change your mind. Goodbye!")
        return

    bot_print("Great! Let's start with your journey details.")

    # 1. Get Origin
    bot_print("Please enter the station code of your *departure station* (e.g., SBC, NDLS).")
    origin = get_valid_input("Enter a valid station code (e.g., SBC).", validate_station_code)
    origin = origin.upper() # Standardize

    # 2. Get Destination
    bot_print(f"Got it ({origin}). Now, please enter the station code of your *destination station* (e.g., MAS, MMCT).")
    destination = get_valid_input("Enter a valid station code (e.g., MAS).", validate_station_code)
    destination = destination.upper()

    # 3. Get Date
    bot_print("Okay. On which *date* would you like to travel? (Please use DD-MM-YYYY format).")
    travel_date = get_valid_input("Enter the date in DD-MM-YYYY format.", validate_date)

    # 4. Find Trains (Simulated)
    bot_print(f"Thank you. I'm searching for trains from {origin} to {destination} for {travel_date}...")
    time.sleep(1) # Simulate search time

    route_key = f"{origin}-{destination}"
    available_trains = train_data.get(route_key, {}).get(travel_date)

    if not available_trains:
        bot_print(f"Sorry, I couldn't find any trains for this route/date in my current data. Please try different stations or dates.")
        return

    # 5. Display Trains
    bot_print(f"Here are the trains available on {travel_date}:")
    for i, train in enumerate(available_trains):
        print(f"  {i+1}. Train {train['no']} - {train['name']} (Dep: {train['dep']}, Arr: {train['arr']})")

    bot_print("Please select the train you are interested in by entering its *number (1, 2, 3...)* from the list above.")

    while True:
        choice = get_valid_input("Enter the list number (e.g., 1).", lambda x: x.isdigit() and 1 <= int(x) <= len(available_trains))
        selected_train_index = int(choice) - 1
        selected_train = available_trains[selected_train_index]
        bot_print(f"You selected: Train {selected_train['no']} - {selected_train['name']}")
        break

    # 6. Select Class
    bot_print("Now, please choose your preferred travel class. Available classes:")
    available_classes = list(selected_train['classes'].keys())
    for i, cls in enumerate(available_classes):
        print(f"  {i+1}. {cls}")

    bot_print("Enter the *number (1, 2, 3...)* corresponding to your desired class.")

    while True:
        choice = get_valid_input("Enter the list number for the class.", lambda x: x.isdigit() and 1 <= int(x) <= len(available_classes))
        selected_class_index = int(choice) - 1
        selected_class_code = available_classes[selected_class_index]
        bot_print(f"You selected class: {selected_class_code}")
        break

    # 7. Display Availability & Fare
    bot_print(f"Checking availability and fare for {selected_class_code} on train {selected_train['no']}...")
    time.sleep(0.5)

    class_details = selected_train['classes'][selected_class_code]
    availability = class_details['avail']
    fare_per_adult = class_details['fare']

    bot_print(f"For {selected_class_code} on {travel_date}:")
    bot_print(f"  Availability Status: **{availability}**")
    bot_print(f"  Estimated Fare per Adult: **₹{fare_per_adult}**")

    bot_print("Would you like to proceed with this option? (yes/no)")
    proceed = get_valid_input("Please answer 'yes' or 'no'.", validate_yes_no)

    if proceed.lower() not in ['yes', 'y']:
        bot_print("Okay, search cancelled. Let me know if you want to start over.")
        return

    # 8. Number of Passengers
    bot_print("How many people will be travelling?")
    bot_print("Enter number of *Adults*:")
    adults = int(get_valid_input("Enter a number.", validate_integer))
    bot_print("Enter number of *Children* (Age 5-11 years, require ticket):")
    children = int(get_valid_input("Enter a number.", validate_integer))
    # Note: Child fare calculation is simplified here (assuming same fare as adult)
    # Real IRCTC has different rules/fares for children.

    total_fare = (adults + children) * fare_per_adult # Simplified calculation
    bot_print(f"Okay, for {adults} Adults and {children} Children, the total estimated fare is **₹{total_fare}**.")
    bot_print("(Note: Fares are indicative and final price depends on dynamic pricing, quotas, etc.)")

    # 9. Nearby Stations (Optional)
    bot_print("\nBefore proceeding to passenger details, would you like to know about other railway stations near your departure or destination station? (yes/no)")
    ask_nearby = get_valid_input("Please answer 'yes' or 'no'.", validate_yes_no)

    if ask_nearby.lower() in ['yes', 'y']:
        bot_print("Which one would you like to check? Enter 'departure' or 'destination'.")
        choice = get_valid_input("Enter 'departure' or 'destination'.", lambda x: x.lower() in ['departure', 'destination'])
        station_to_check = origin if choice.lower() == 'departure' else destination
        nearby_list = nearby_stations_data.get(station_to_check)
        if nearby_list:
            bot_print(f"Some stations near {station_to_check}:")
            for station in nearby_list:
                print(f" - {station}")
        else:
            bot_print(f"Sorry, I don't have nearby station information for {station_to_check} in my data.")

    # 10. Handoff for Booking
    bot_print("\nTo complete your booking, you'll need to provide passenger details (name, age, gender, berth preference) and make the payment.")
    bot_print("As an assistant bot, I cannot securely collect these details or process payments.")
    bot_print("Please proceed to the official IRCTC website (www.irctc.co.in) or the IRCTC Rail Connect app using your login to finalize this booking.")
    bot_print("You will need the details: Train " + selected_train['no'] + ", Date " + travel_date + ", Class " + selected_class_code + ", From " + origin + " To " + destination + ".")

    bot_print("\nThank you for using the IRCTC booking assistant! Have a safe journey!")

# --- Start the Chatbot ---
if __name__ == "__main__":
    run_chatbot()
