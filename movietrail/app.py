'''from flask import Flask, jsonify, render_template,request
import requests

app = Flask(__name__)

@app.route('/movies', methods=['GET'])
def get_movies():
    return render_template('movies.html')
    url = "https://imdb-top-100-movies1.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
        "X-RapidAPI-Host": "imdb-top-100-movies1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        movie_data = response.json()

        movies = []
        for movie in movie_data:
            movie_name = movie.get("title")
            movie_description = movie.get("description")
            movie_rating = movie.get("rating")
            movie_year = movie.get("year")
            movie_thumbnail = movie.get("thumbnail")
            movie_genre = movie.get("genre")

            # Check if the thumbnail is available, otherwise use a fallback image
            if movie_thumbnail:
                thumbnail_url = movie_thumbnail
            else:
                thumbnail_url = "/static/images/fallback.jpg"  # Path to a fallback image

            movie_info = {
                "name": movie_name,
                "description": movie_description,
                "rating": movie_rating,
                "year": movie_year,
                "thumbnail": thumbnail_url,
                "genre":movie_genre
            }
            movies.append(movie_info)

        return render_template('movies.html', movies=movies)
    else:
        return jsonify({'error': 'Failed to retrieve movie data'})




@app.route('/search', methods=['GET'])
def search_movies():
    search_query = request.args.get('search')

    url = "https://advanced-movie-search.p.rapidapi.com/search/movie"
    querystring = {"query": search_query, "page": "1"}

    headers = {
        "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
        "X-RapidAPI-Host": "advanced-movie-search.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        search_results = response.json()
        return render_template('movies.html', search_results=search_results, search_query=search_query)
    else:
        return jsonify({'error': 'Failed to retrieve movie search results'})




if __name__ == '__main__':
    app.run(debug=True)
'''

# after some minor changes 

from flask import Flask, render_template, request, redirect, session,jsonify
import requests

app = Flask(__name__)

app.secret_key = 'your_secret_key_here'
valid_api_key = "lRJUCySxN1Euri6OAFsqkJl5JJ0Tj6ce"  
# api authentication part of the web
@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        api_key = request.form.get('api_key')
        if api_key == valid_api_key:
            session['api_key'] = api_key 
            return redirect('/movies')
        else:
            return render_template('landing.html', error='Invalid API Key')
    return render_template('landing.html')

# retreiving the data from the api 
@app.route('/movies', methods=['GET'])
# def get_movies():
#     return render_template('movies.html')
def get_movies():
    url = "https://imdb-top-100-movies1.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
        "X-RapidAPI-Host": "imdb-top-100-movies1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        movie_data = response.json()

        movies = []
        for movie in movie_data:
            movie_name = movie.get("title") # taking some of the information from the api and displaying
            movie_description = movie.get("description")
            movie_rating = movie.get("rating")
            movie_year = movie.get("year")
            movie_thumbnail = movie.get("thumbnail")
            movie_genre = movie.get("genre")
            if movie_thumbnail:
                thumbnail_url = movie_thumbnail
            else:
                thumbnail_url = "/static/images/fallback.jpg" 

            movie_info = {
                "name": movie_name,
                "description": movie_description,
                "rating": movie_rating,
                "year": movie_year,
                "thumbnail": thumbnail_url,
                "genre": movie_genre
            }
            movies.append(movie_info)

        return render_template('movies.html', movies=movies)

    return jsonify({'error': 'Failed to retrieve movie data'})

# this part comes for the search of the desired movies from the api

@app.route('/search', methods=['GET'])
def search_movies():
    search_query = request.args.get('search')

    if search_query:
        url = "https://advanced-movie-search.p.rapidapi.com/search/movie"
        querystring = {"query": search_query, "page": "1"}

        headers = {
            "X-RapidAPI-Key": "d3990f018emshcb4637527c98346p1a395ajsn9092289ff168",
            "X-RapidAPI-Host": "advanced-movie-search.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            search_results = response.json()
            movies = []
            for movie in search_results['results']:
                movies.append({
                    'title': movie['title'],
                    'year': movie['release_date'],
                    'rating': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                })
            return render_template('display.html', movies=movies, query=search_query)

    return jsonify({'error': 'Failed to retrieve movie search results'})

API_KEY = "lRJUCySxN1Euri6OAFsqkJl5JJ0Tj6ce"

@app.route('/your-endpoint', methods=['GET'])
def your_endpoint():
    api_key = request.headers.get('X-API-Key')
    if api_key == API_KEY:
        return f"The API key is: {API_KEY}. Proceed with further processing."
    
    else:
        return 'Invalid API Key.', 401 



if __name__ == '__main__':
    app.run(debug=True)







