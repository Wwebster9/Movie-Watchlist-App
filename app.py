import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie.
5) View watched movies.
6) Add user to the app.
7) Search for a movie.
8) Exit.

Your selection: """
welcome = "\nWelcome to the movie watchlist app!"


# print welcome message and create empty tables
print(welcome)
database.create_tables()


def prompt_add_movies():
    title = input("Movie title: ")
    # date must match this format
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()
    database.add_movie(title, timestamp)


def print_movie_list(heading, movie_list):
    print(f"\n----- {heading} movies -----\n")
    # _id used because id is a built-in function and don't want to overwrite that function
    for _id, title, release_date in movie_list:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} on {human_date}")
    print("\n----- End of list -----\n")


def prompt_watch_movie():
    username = input("Username: ")
    movie_id = input("Movie ID: ")
    database.watch_movie(username, movie_id)


def prompt_show_watched_movies():
    username = input("Username: ")
    watched_movies = database.get_watched_movies(username)
    if movies:
        print_movie_list("Watched", watched_movies)
    else:
        print("No watched movies for that user")


def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)


def prompt_search_movies():
    search_term = input("Enter your search term: ")
    searched_movies = database.search_movies(search_term)
    if searched_movies:
        print_movie_list("Found", searched_movies)
    else:
        print("No movies found for that search term")


while (user_input := input(menu)) != "8":
    if user_input == "1":
        prompt_add_movies()
    elif user_input == "2":
        movies = database.get_movies(upcoming=True)
        print_movie_list("Upcoming", movies)
    elif user_input == "3":
        movies = database.get_movies()
        print_movie_list("All", movies)
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        prompt_show_watched_movies()
    elif user_input == "6":
        prompt_add_user()
    elif user_input == "7":
        prompt_search_movies()
    else:
        print("Invalid input, please try again!")
