#
# Simple script to search for random terms on Bing
#
import webbrowser
import time
import urllib.parse
import random


def main():
    # Define a list of ten search terms
    search_terms = [
        "New York weather",
        "Kyle McCann stats",
        "Wendy's near me",
        "Top Python libraries",
        "New York Jets quarterback news",
        "How to start a garden",
        "Best 2024 movies",
        "Smart home devices 2024",
        "Python tutorials for beginners",
        "NHL standings 2024",
        "Upcoming technology innovations",
        "Katya Clover images",
        "Healthy recipes",
        "DIY home improvement ideas",
        "MLB standing 2024",
        "NFL draft 2024",
        "Financial planning tips",
        "Gloria Sol images",
        "Lorena Garcia images",
        "Best 2024 TV shows",
        "Best 2024 movies",
        "Pizza near me",
        "How to make a pizza",
        "Open source LLM tools",
        "No code tools",
        "Best 2024 books",
        "Avery Nona images",
        "Mt. Snow ski conditions",
        "Stowe ski conditions",
        "Okemo ski conditions",
        "Hunter ski conditions",
        "Big Boulder ski conditions",
        "Jack Frost ski conditions",
        "Epic Pass 2024",
        "Heavenly Valley ski conditions",
        "weather in tashkent",
        "weather forecast",
        "stalker 2 tips and tricks",
        "Movies near me",
        "Shop for milk and eggs",
        "rust dioxus tutorial",
        "how do I boil an egg",
        "healthy recipes",
        "how to make a pizza",
        "how to make a cake",
        "Implement Stripe Payouts",
        "Stripe API documentation",
        "Stripe python SDK",
        "Flights to DTW",
        "Stalker 2 walkthrough",
        "Things to do in Puerto Rico",
    ]

    # Randomly selec search terms from the list
    selected_terms = random.sample(search_terms, 30)

    # Search each selected term on Bing
    for term in selected_terms:
        print(f"Searching for: {term}")
        try:
            query_encoded = urllib.parse.quote_plus(term)
            url = f"https://www.bing.com/search?q={query_encoded}"
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open URL for term '{term}': {e}")
        time.sleep(5)  # Wait for 5 seconds


if __name__ == "__main__":
    main()
