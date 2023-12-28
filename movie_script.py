import requests

api_key = 'bc4279975ab32796e9a2477325d3d5dd'
OMDB_API_KEY = '3ce57d37'
OMDB_API_URL = 'http://www.omdbapi.com/'
base_url = 'https://api.themoviedb.org/3'

def search_movie(query):
    search_endpoint = '/search/movie'
    url = f'{base_url}{search_endpoint}?api_key={api_key}&query={query}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data and data['results']:
        movie_id = data['results'][0]['id']
        return get_movie_details(movie_id)
    else:
        return None

def get_movie_details(movie_id):
    details_endpoint = f'/movie/{movie_id}'
    credits_endpoint = f'/movie/{movie_id}/credits'
    url_details = f'{base_url}{details_endpoint}?api_key={api_key}'
    url_credits = f'{base_url}{credits_endpoint}?api_key={api_key}'
    details_response = requests.get(url_details)
    credits_response = requests.get(url_credits)
    details_data = details_response.json()
    credits_data = credits_response.json()
    genres = [genre['name'] for genre in details_data['genres']]
    keywords = [keyword['name'] for keyword in details_data.get('keywords', {}).get('keywords', [])]
    title = details_data['title']
    overview = details_data['overview']
    original_language = details_data['original_language']
    poster_path = details_data['poster_path'] if 'poster_path' in details_data else None
    # Extracting cast and crew information
    cast = [{'name': actor['name'], 'character': actor['character']} for actor in credits_data['cast'][:5]]
    crew = [{'name': member['name'], 'job': member['job']} for member in credits_data['crew'] if member['job'] == 'Director'][:1]
    omdb_url = f'{OMDB_API_URL}?t={title}&apikey={OMDB_API_KEY}'
    omdb_response = requests.get(omdb_url)
    omdb_data = omdb_response.json()
    imdb_rating = omdb_data.get('imdbRating', 'Not available')


    return {
        'id': movie_id,
        'title': title,
        'genres': genres,
        'keywords': keywords,
        'overview': overview,
        'imdb_rating': imdb_rating,
        'original_language': original_language,
        'cast': cast,
        'crew': crew,
        'poster_path': poster_path
    }

def recommend_movies(movie_id):
    recommendation_endpoint = f'/movie/{movie_id}/recommendations'
    url_recommendations = f'{base_url}{recommendation_endpoint}?api_key={api_key}'
    response = requests.get(url_recommendations)
    data = response.json()
    recommended_movies = []
    for result in data.get('results', []):
        if result['id'] != movie_id:
            recommended_movies.append({
                'title': result['title'],
                'poster_path': result['poster_path'] if 'poster_path' in result else None
            })
    return recommended_movies[:5]


def get_best_movies_of_director(director_name):
    search_query = director_name.replace(' ', '+')
    search_endpoint = '/search/person'
    url = f'{base_url}{search_endpoint}?api_key={api_key}&query={search_query}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data and data['results']:
        person_id = data['results'][0]['id']
        movies_endpoint = f'/person/{person_id}/movie_credits'
        url_movies = f'{base_url}{movies_endpoint}?api_key={api_key}'
        response = requests.get(url_movies)
        data = response.json()
        movies = []
        for movie in data.get('cast', []):
            if movie['vote_average'] is not None and movie['vote_average'] >= 7:
                movies.append({
                    'title': movie['title'],
                    'poster_path': movie['poster_path'] if 'poster_path' in movie else None
                })
        return movies[:2]
    else:
        return []

def get_best_movies_of_actor(actor_name):
    search_query = actor_name.replace(' ', '+')
    search_endpoint = '/search/person'
    url = f'{base_url}{search_endpoint}?api_key={api_key}&query={search_query}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data and data['results']:
        person_id = data['results'][0]['id']
        movies_endpoint = f'/person/{person_id}/movie_credits'
        url_movies = f'{base_url}{movies_endpoint}?api_key={api_key}'
        response = requests.get(url_movies)
        data = response.json()
        movies = []
        for movie in data.get('cast', []):
            if movie['vote_average'] is not None and movie['vote_average'] >= 7:
                movies.append({
                    'title': movie['title'],
                    'poster_path': movie['poster_path'] if 'poster_path' in movie else None
                })
        return movies[:2]
    else:
        return []

def get_best_movie_of_actress(actress_name):
    search_query = actress_name.replace(' ', '+')
    search_endpoint = '/search/person'
    url = f'{base_url}{search_endpoint}?api_key={api_key}&query={search_query}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data and data['results']:
        person_id = data['results'][0]['id']
        movies_endpoint = f'/person/{person_id}/movie_credits'
        url_movies = f'{base_url}{movies_endpoint}?api_key={api_key}'
        response = requests.get(url_movies)
        data = response.json()
        movies = []
        for movie in data.get('cast', []):
            if movie['vote_average'] is not None and movie['vote_average'] >= 7:
                movies.append({
                    'title': movie['title'],
                    'poster_path': movie['poster_path'] if 'poster_path' in movie else None
                })
        return movies[:1]
    else:
        return []


if __name__ == '__main__':
    search_query = input("Enter a movie title to search: ")
    movie_details = search_movie(search_query)

    if movie_details:
        print(f"Poster: https://image.tmdb.org/t/p/original{movie_details['poster_path']}")
        print("\nMovie Details:")
        print(f"Title: {movie_details['title']}")
        print(f"Genres: {', '.join(movie_details['genres'])}")
        print(f"Keywords: {', '.join(movie_details['keywords'])}")
        print(f"Rating: {movie_details['imdb_rating']}")
        print(f"ID: {movie_details['id']}")
        print(f"Overview: {movie_details['overview']}")
        print(f"Original Language: {movie_details['original_language']}")
        
        print("\nCast:")
        for actor in movie_details['cast']:
            print(f"{actor['name']}")

        print("\nCrew:")
        for member in movie_details['crew']:
            print(f"{member['name']}")
        
        # Recommend movies based on the searched movie
        recommendations = recommend_movies(movie_details['id'])
        if not recommendations:
            director_name = movie_details['crew'][0]['name']
            actor_names = [actor['name'] for actor in movie_details['cast'][:2]]
            # Ensure that the lists have values before attempting to access elements
            director_name = director_name if director_name else None
            actor_name = actor_names[0] if actor_names else None
            actress_name = actor_names[1] if actor_names else None

        # Create a list to store all recommended movies
        recommended_movies = []

        # Get 2 best movies of director
        if director_name:
            director_movies = get_best_movies_of_director(director_name)
            for i, movie in enumerate(director_movies, start=1):
                recommended_movies.append(f"{i}. {movie}")

        # Get 2 best movies of actors
        for actor_name in actor_names:
            if actor_name:
                actor_movies = get_best_movies_of_actor(actor_name)
                for i, movie in enumerate(actor_movies, start=1):
                    recommended_movies.append(f"{i}. {movie}")

        if actress_name:
            actress_movie = get_best_movie_of_actress(actress_name)
            recommended_movies.append(f"1. {actress_movie}")

        # Print all recommended movies
        print("\nRecommended Movies:")
        for movie in recommended_movies:
            print(movie)


            
        else:
            print("\nRecommended Movies:")
            for i, movie in enumerate(recommendations, start=1):
                print(f"{i}. {movie}")
    else:
        print("No movie found.")
