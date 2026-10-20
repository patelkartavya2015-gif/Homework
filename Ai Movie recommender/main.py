import csv
import random
import re
from pathlib import Path
from textwrap import fill

from colorama import Fore, Style, init

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None


DATA_PATH = Path(__file__).with_name("imdb_top_1000.csv")
init(autoreset=True)

POSITIVE_WORDS = {
    "adventure", "beautiful", "brave", "bond", "courage", "decency", "enjoy",
    "friend", "good", "happy", "hope", "joy", "love", "redemption", "solace",
    "success", "triumph", "wonderful",
}
NEGATIVE_WORDS = {
    "abuse", "death", "despair", "evil", "fear", "grief", "hate", "imprisoned",
    "loss", "murder", "pain", "revenge", "sad", "suffering", "tragedy", "violence",
    "violent", "war",
}


def ask(prompt):
    return input(f"{Fore.YELLOW}{Style.BRIGHT}{prompt}{Style.RESET_ALL}").strip()


def show_header():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 58}")
    print("  THE MOVIE FINDER")
    print(f"{'=' * 58}{Style.RESET_ALL}")


def fallback_polarity(text):
    words = re.findall(r"[a-z']+", text.lower())
    score = sum(word in POSITIVE_WORDS for word in words)
    score -= sum(word in NEGATIVE_WORDS for word in words)
    return score / max(len(words), 1)


def sentiment_for(text):
    if TextBlob is not None:
        polarity = TextBlob(text).sentiment.polarity
    else:
        polarity = fallback_polarity(text)
    if polarity > 0.02:
        return "positive", polarity
    if polarity < -0.02:
        return "negative", polarity
    return "neutral", polarity


def load_movies():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Movie dataset not found: {DATA_PATH}")

    with DATA_PATH.open(encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        required_columns = {"Series_Title", "Genre", "Overview", "IMDB_Rating"}
        missing_columns = required_columns - set(reader.fieldnames or [])
        if missing_columns:
            raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing_columns))}")

        movies = []
        for row in reader:
            try:
                rating = float(row["IMDB_Rating"])
            except (TypeError, ValueError):
                continue

            overview = (row.get("Overview") or "").strip()
            mood, polarity = sentiment_for(overview)
            movies.append({
                "title": (row.get("Series_Title") or "Untitled").strip(),
                "genres": [genre.strip() for genre in (row.get("Genre") or "").split(",") if genre.strip()],
                "overview": overview or "No overview available.",
                "rating": rating,
                "mood": mood,
                "polarity": polarity,
            })
    return movies


def ask_mode():
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Choose a recommendation type:")
        print(f"  {Fore.GREEN}1  AI-based match{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}2  Random pick{Style.RESET_ALL}")
        choice = ask("Select 1 or 2: ").lower()
        if choice in {"1", "ai", "a", "ai-based recommendation"}:
            return "ai"
        if choice in {"2", "random", "r", "random recommendation"}:
            return "random"
        print(f"{Fore.RED}Please choose 1 for AI-based or 2 for Random.")


def ask_genre(genres):
    print(f"{Fore.CYAN}Available genres: {Fore.GREEN}" + ", ".join(genres))
    while True:
        choice = ask("Preferred genre (or 'any'): ")
        if choice.lower() in {"", "any", "all", "skip"}:
            return None
        match = next((genre for genre in genres if genre.casefold() == choice.casefold()), None)
        if match:
            return match
        print(f"{Fore.RED}Please enter a genre from the list, or 'any'.")


def ask_mood():
    aliases = {
        "positive": "positive", "happy": "positive", "upbeat": "positive", "hopeful": "positive",
        "negative": "negative", "sad": "negative", "dark": "negative", "tense": "negative",
        "neutral": "neutral", "calm": "neutral", "balanced": "neutral",
    }
    while True:
        choice = ask("Preferred mood (positive/neutral/negative, or 'any'): ").casefold()
        if choice in {"", "any", "all", "skip"}:
            return None
        if choice in aliases:
            return aliases[choice]
        print(f"{Fore.RED}Choose positive, neutral, negative, or any.")


def ask_rating():
    while True:
        choice = ask("Minimum IMDb rating from 0 to 10 (or press Enter to skip): ")
        if not choice:
            return None
        try:
            rating = float(choice)
        except ValueError:
            print(f"{Fore.RED}Enter a number from 0 to 10, or press Enter to skip.")
            continue
        if 0 <= rating <= 10:
            return rating
        print(f"{Fore.RED}Rating must be between 0 and 10.")


def get_ai_recommendation(movies, seen_titles):
    genres = sorted({genre for movie in movies for genre in movie["genres"]})
    preferred_genre = ask_genre(genres)
    preferred_mood = ask_mood()
    minimum_rating = ask_rating()

    matches = [
        movie for movie in movies
        if (preferred_genre is None or preferred_genre in movie["genres"])
        and (preferred_mood is None or preferred_mood == movie["mood"])
        and (minimum_rating is None or movie["rating"] >= minimum_rating)
    ]
    if not matches:
        print(f"{Fore.RED}No movies match those preferences. Try a broader genre, mood, or rating.")
        return None

    unseen = [movie for movie in matches if movie["title"] not in seen_titles]
    candidates = unseen or matches
    candidates.sort(key=lambda movie: movie["rating"], reverse=True)
    print(f"{Fore.CYAN}Found {len(matches)} match(es); picking from the highest-rated results.")
    return random.choice(candidates[:min(5, len(candidates))])


def get_random_recommendation(movies, seen_titles):
    unseen = [movie for movie in movies if movie["title"] not in seen_titles]
    return random.choice(unseen or movies)


def show_movie(movie):
    width = 64
    mood_colors = {"positive": Fore.GREEN, "neutral": Fore.YELLOW, "negative": Fore.RED}
    rating_bar = "#" * round(movie["rating"]) + "-" * (10 - round(movie["rating"]))

    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * width}")
    print(f"{Fore.WHITE}{Style.BRIGHT}{movie['title']}")
    print(f"{Fore.CYAN}{'-' * width}")
    print(f"{Fore.GREEN}Genre(s): {Style.RESET_ALL}{', '.join(movie['genres']) or 'Not listed'}")
    print(f"{Fore.WHITE}Overview: {fill(movie['overview'], width=width)}")
    print(
        f"{Fore.YELLOW}IMDb Rating: {movie['rating']:.1f}/10  "
        f"{Fore.GREEN}{rating_bar}"
    )
    print(
        f"{Fore.WHITE}Sentiment: "
        f"{mood_colors[movie['mood']]}{movie['mood'].capitalize()} "
        f"{Fore.WHITE}(polarity {movie['polarity']:+.2f})"
    )
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * width}")


def ask_to_continue():
    while True:
        answer = ask("Would you like another recommendation? (yes/no): ").casefold()
        if answer in {"yes", "y"}:
            return True
        if answer in {"no", "n"}:
            return False
        print(f"{Fore.RED}Please answer yes or no.")


def main():
    try:
        movies = load_movies()
    except (FileNotFoundError, ValueError) as error:
        print(f"{Fore.RED}Error: {error}")
        return
    if not movies:
        print(f"{Fore.RED}Error: The movie dataset contains no usable entries.")
        return

    show_header()
    print(f"{Fore.CYAN}Loaded {Fore.GREEN}{len(movies)}{Fore.CYAN} movies from the IMDb dataset.")
    name = ask("What's your name? ") or "Movie fan"
    print(f"{Fore.GREEN}{Style.BRIGHT}Welcome, {name}. Let's find your next movie.")

    seen_titles = set()
    while True:
        mode = ask_mode()
        if mode == "ai":
            movie = get_ai_recommendation(movies, seen_titles)
        else:
            movie = get_random_recommendation(movies, seen_titles)

        if movie:
            show_movie(movie)
            seen_titles.add(movie["title"])
        if not ask_to_continue():
            print(f"{Fore.CYAN}Thanks for stopping by, {name}. Enjoy the movie!")
            break


if __name__ == "__main__":
    main()