import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify

# Initialize the flask app
app = Flask(__name__)

# --- Load the saved model objects ---
# We load the pivot table (pt) and titles from their pickled files
pt = pd.DataFrame(pickle.load(open('pt.pkl', 'rb')))
book_titles = pickle.load(open('book_titles.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# We load book_info as a DataFrame
book_info = pd.DataFrame(pickle.load(open('book_info.pkl', 'rb')))

# Route for the main home page
@app.route('/')
def home():
    # Pass the list of book titles to the frontend
    return render_template('index.html', book_titles=book_titles)

# Route for the recommendation API
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Get the book name from the form data
        book_name = request.form.get('book_name')

        # Find the index of the book
        index = np.where(pt.index == book_name)[0][0]

        # Get similarity scores and find top 5
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        recommended_books_data = []
        for item in similar_items:
            temp_book_title = pt.index[item[0]]

            # Get details from book_info DataFrame
            book_details = book_info[book_info['Book-Title'] == temp_book_title].iloc[0]

            recommended_books_data.append({
                'Book-Title': book_details['Book-Title'],
                'Book-Author': book_details['Book-Author'],
                'Image-URL-M': book_details['Image-URL-M']
            })

        # Return the recommendations as a JSON object
        return jsonify(recommended_books_data)

    except Exception as e:
        # Handle errors (e.g., book not found)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)