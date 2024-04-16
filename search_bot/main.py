import webbrowser
import sys
import urllib.parse

def main():

    search_term = "MLB standings 2024"
    query_encoded = urllib.parse.quote_plus(search_term)
    url = f"https://www.bing.com/search?q={query_encoded}"

    webbrowser.open(url)

if __name__ == "__main__":
    main()
