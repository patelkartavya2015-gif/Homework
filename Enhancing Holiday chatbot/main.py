import re, colorama, random
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from colorama import Fore, init



init(autoreset = True)



destinations = {
    "beaches" : ["Bali", "Maldives", "Hawaii", "Phuket", "Bahamas"],
    "mountains" : ["Swiss Alps", "Rocky Mountains", "Himalayas", "Andes", "Dolomites"],
    "cities" : ["New York", "Paris", "Tokyo", "London", "Sydney"],
}

jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why did the bicycle fall over? Because it was two-tired!",
]

simulated_weather = {
    "Bali": ["Warm and sunny, around 29 C", "Tropical showers, around 27 C"],
    "Maldives": ["Sunny with a light sea breeze, around 30 C", "Partly cloudy, around 28 C"],
    "Hawaii": ["Bright skies with gentle trade winds, around 26 C", "Passing showers, around 25 C"],
    "Phuket": ["Hot and humid with a chance of showers, around 30 C", "Mostly sunny, around 29 C"],
    "Bahamas": ["Sunny and breezy, around 27 C", "Partly cloudy, around 26 C"],
    "Swiss Alps": ["Cool with clear mountain skies, around 12 C", "Cloudy with a chance of snow, around 4 C"],
    "Rocky Mountains": ["Crisp and sunny, around 15 C", "Afternoon showers, around 10 C"],
    "Himalayas": ["Cool and clear, around 11 C", "Windy with high-altitude clouds, around 7 C"],
    "Andes": ["Mild and sunny, around 17 C", "Cool with scattered showers, around 13 C"],
    "Dolomites": ["Pleasant and clear, around 16 C", "Light mountain rain, around 9 C"],
    "New York": ["Partly cloudy, around 21 C", "Light rain, around 17 C"],
    "Paris": ["Mild with sunny breaks, around 19 C", "Cloudy with light showers, around 16 C"],
    "Tokyo": ["Warm and mostly sunny, around 23 C", "Cloudy with a chance of rain, around 20 C"],
    "London": ["Cool with a few sunny spells, around 16 C", "Light showers, around 14 C"],
    "Sydney": ["Sunny with a coastal breeze, around 22 C", "Partly cloudy, around 19 C"],
}

city_timezones = {
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "honolulu": "Pacific/Honolulu",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "tokyo": "Asia/Tokyo",
    "sydney": "Australia/Sydney",
    "dubai": "Asia/Dubai",
    "singapore": "Asia/Singapore",
}

travel_news = [
    "Simulated update: A new coastal trail is opening for visitors this season.",
    "Simulated update: Several museums are extending evening hours for travelers.",
    "Simulated update: A regional rail pass now covers more scenic routes.",
    "Simulated update: Local markets are hosting weekend food and craft festivals.",
]



def normalize_input(user_input):
    return re.sub(r"\s+", " ", user_input.strip().lower())


def recommend():
    while True:
        print(Fore.CYAN + "Travel bot: Choose beaches, mountains, or cities (or 'back' to return).")
        preference = normalize_input(input(Fore.GREEN + "You: "))
        if preference == "back":
            return
        if preference not in destinations:
            print(Fore.RED + "Travel bot: Choose beaches, mountains, or cities.")
            continue

        suggestion = random.choice(destinations[preference])
        print(Fore.CYAN + f"Travel bot: I recommend visiting {suggestion}!")
        answer = normalize_input(input(Fore.GREEN + "Travel bot: Want another suggestion? (yes/no)\nYou: "))
        if answer != "yes":
            print(Fore.CYAN + "Travel bot: Have a wonderful trip!")
            return

def packing():
    trip_type = normalize_input(input(Fore.CYAN + "Travel bot: What kind of trip? (beach/mountain/city)\nYou: "))
    if trip_type not in {"beach", "mountain", "city"}:
        print(Fore.RED + "Travel bot: Please choose beach, mountain, or city.")
        return

    try:
        days = int(input(Fore.CYAN + "Travel bot: How many days?\nYou: "))
        if days < 1:
            raise ValueError
    except ValueError:
        print(Fore.RED + "Travel bot: Enter a number of days greater than zero.")
        return

    essentials = ["Versatile clothes", "Travel adapter", "Personal medication", "Travel documents"]
    extras = {
        "beach": ["Swimwear", "Sunscreen", "Sandals"],
        "mountain": ["Sturdy hiking shoes", "Warm layers", "Reusable water bottle"],
        "city": ["Comfortable walking shoes", "Day bag", "Transit card or app"],
    }
    print(Fore.GREEN + f"Travel bot: Packing list for a {days}-day {trip_type} trip:")
    for item in essentials + extras[trip_type]:
        print(Fore.GREEN + f"- {item}")
    print(Fore.GREEN + "Check the local forecast before you leave, and pack enough outfits for your trip.")

def tell_joke():
    print(Fore.CYAN + "Travel bot: Here's a joke for you:", Fore.YELLOW + random.choice(jokes))


def show_help():
    print(Fore.MAGENTA + "\nTry a command:")
    print(Fore.CYAN + "recommend | pack | weather | news | time | joke | help | exit")


def show_weather():
    city = input(Fore.CYAN + "Travel bot: Which destination?\nYou: ").strip()
    match = next((name for name in simulated_weather if name.lower() == city.lower()), None)
    if match is None:
        choices = ", ".join(simulated_weather)
        print(Fore.RED + f"Travel bot: I can simulate weather for these destinations: {choices}.")
        return
    condition = random.choice(simulated_weather[match])
    print(Fore.CYAN + f"Travel bot: Simulated weather for {match}: {condition}. This is not a live forecast.")


def show_news():
    print(Fore.CYAN + "Travel bot: Here is a simulated travel update (not live news):")
    print(Fore.YELLOW + random.choice(travel_news))


def show_local_time():
    city = normalize_input(input(Fore.CYAN + "Travel bot: Which city?\nYou: "))
    timezone_name = city_timezones.get(city)
    if timezone_name is None:
        choices = ", ".join(city.title() for city in city_timezones)
        print(Fore.RED + f"Travel bot: I can show the time for: {choices}.")
        return
    try:
        local_time = datetime.now(ZoneInfo(timezone_name))
    except ZoneInfoNotFoundError:
        print(Fore.RED + "Travel bot: Time zone data is unavailable in this Python installation.")
        return
    print(Fore.CYAN + f"Travel bot: The local time in {city.title()} is {local_time:%A, %B %d, %Y at %I:%M %p}.")


def chat():
    print(Fore.CYAN + "Travel bot: Hello! I'm your travel assistant. How can I help you today? Please enter your name:")
    name = input(Fore.GREEN + "You: ").strip() or "traveler"
    print(Fore.CYAN + f"Travel bot: Nice to meet you, {name}!")
    show_help()
    while True:
        userinput = normalize_input(input(Fore.GREEN + "You: "))
        if userinput == "recommend":
            recommend()
        elif userinput in {"pack", "packing"}:
            packing()
        elif userinput == "weather":
            show_weather()
        elif userinput == "news":
            show_news()
        elif userinput in {"time", "local time"}:
            show_local_time()
        elif userinput == "joke":
            tell_joke()
        elif userinput == "help":
            show_help()
        elif userinput == "exit":
            print(Fore.CYAN + "Travel bot: Goodbye! Have a great trip!")
            break
        else:
            print(Fore.RED + "Travel bot: I didn't recognize that command. Type 'help' to see what I can do.")


if __name__ == "__main__":
    chat()