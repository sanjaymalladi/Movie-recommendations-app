from flask import Flask, render_template, request
import movie_script

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query']
        movie_details = movie_script.search_movie(search_query)

        if movie_details:
            recommendations = movie_script.recommend_movies(movie_details['id'])
            return render_template('result.html', movie_details=movie_details, recommendations=recommendations)
        else:
            return render_template('no_result.html')

if __name__ == '__main__':
    app.run(debug=True)
