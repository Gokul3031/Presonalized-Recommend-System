import streamlit as st
import numpy as np
import pickle

# Function to load the pickle files
def load_pickle(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)

# Function to fetch the details for the recommended books
def fetch_book_details(suggestions, book_pivot, final_rating):
    book_details = []
    for book_id in suggestions[0]:
        book_title = book_pivot.index[book_id]
        book_row = final_rating.loc[final_rating['title'] == book_title].iloc[0]
        
        # Fetch the number of ratings and normalize it if available
        if 'num_of_rating' in book_row:
            total_ratings = book_row['num_of_rating']
            normalized_rating = total_ratings / max(final_rating['num_of_rating']) * 5
            rating_str = '⭐' * int(np.ceil(normalized_rating))
        else:
            rating_str = "Unknown"
        
        details = {
            'title': book_title,
            'author': book_row.get('author', 'Unknown Author'),
            'year': book_row.get('year', 'Unknown Year'),
            'rating': rating_str,
            'img_url': book_row['img_url']
        }
        book_details.append(details)
    return book_details

# Function to recommend books based on the selected book
def recommend_books(book_name, book_pivot, model, books_name):
    book_id = np.where(books_name == book_name)[0][0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=5)
    return suggestions


# Load your data and model
model_path = "C:\\Users\\gokul\\Desktop\\Constient-project\\Book_recommendation\\recommendation-systems\\model\\"
model = load_pickle(f"{model_path}model.pkl")
books_name = load_pickle(f"{model_path}books_name.pkl")
final_rating = load_pickle(f"{model_path}final_rating.pkl")
book_pivot = load_pickle(f"{model_path}book_pivot.pkl")

# Set up the header for your Streamlit application
st.header("Books Recommendation System 📚")

# Dropdown for selecting the book
selected_book = st.selectbox("Type or select a book from the dropdown", books_name)

# Button to show recommendations
if st.button('Show Recommendation'):
    suggestions = recommend_books(selected_book, book_pivot, model, books_name)
    book_details = fetch_book_details(suggestions, book_pivot, final_rating)

    # Display the recommendations with their posters and details
    for details in book_details:
        # Create a column for each recommended book
        cols = st.columns([1, 3])  # Adjust the ratio as needed for image/text layout

        with cols[0]:  # For the image
            st.image(details['img_url'], width=150)  # Set width to fit your layout
        with cols[1]:  # For the text
            st.subheader(details['title'])
            st.caption(f"Author: {details['author']}")
            st.caption(f"Year: {details['year']}")
            st.caption(f"Rating: {details['rating']}")