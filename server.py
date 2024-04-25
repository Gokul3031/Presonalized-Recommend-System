import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pickle
import logging
from dotenv import load_dotenv
import os
from fast_autocomplete import AutoComplete
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HOST = os.environ["HOST"]
PORT = int(os.environ["PORT"])

# Assuming 'app' is your FastAPI application object, defined in 'my_fastapi_app.py'
app_import_string = "server:app"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static")
, name="static")

def load_pickle(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)

model_path = "model"
model = load_pickle(f"{model_path}\\model.pkl")
books_name = load_pickle(f"{model_path}\\books_name.pkl")
final_rating = load_pickle(f"{model_path}\\final_rating.pkl")
book_pivot = load_pickle(f"{model_path}\\book_pivot.pkl")

books_name_lower = books_name.str.lower().str.strip()  

# books_dict = {str(i): {"word": book.lower()} for i, book in enumerate(books_name_lower)}
books_dict = {book.lower():{} for i, book in enumerate(books_name_lower)}

# print(books_dict)
autocomplete = AutoComplete(words=books_dict)

# @app.on_event("startup")
# async def startup_event():
#     global books_dict
#     autocomplete = AutoComplete(words=books_dict)

@app.get("/autocomplete/{search}")
async def autocomplete_search(search: str):
    search = search.strip().lower()
    print(search)
    return autocomplete.search(word=search, max_cost=3, size=10)


def fetch_book_details(suggestions, book_pivot, final_rating):
    book_details = []
    for book_id in suggestions[0]:
        book_title = book_pivot.index[book_id]
        book_row = final_rating.loc[final_rating['title'] == book_title].iloc[0]

        total_ratings = book_row.get("num_of_rating", 0)
        normalized_rating = float(total_ratings / max(final_rating['num_of_rating'], default=1) * 5)
        rating_str = '⭐' * int(np.ceil(normalized_rating)) if total_ratings else "Unknown"

        details = {
            'title': book_title,
            'author': book_row.get('author', 'Unknown Author'),
            'year': str(book_row.get('year', 'Unknown Year')),
            'rating': rating_str,
            'img_url': book_row['img_url']
        }
        book_details.append(details)
    return book_details

def recommend_books(book_name, book_pivot, model, books_name_lower):
    book_name = book_name.strip().lower()
    # Search for close matches with autocorrect
    corrections = autocomplete.search(word=book_name, max_cost=10, size=10)

    if not corrections:
        raise HTTPException(status_code=404, detail=f"No close matches found for '{book_name}'. Please check your spelling.")

    # Use the closest match
    corrected_book_name = corrections[0][0]
    book_indices = np.where(books_name_lower == corrected_book_name)[0]

    if len(book_indices) == 0:
        raise HTTPException(status_code=404, detail=f"Book '{corrected_book_name}' not found in the dataset.")

    book_id = book_indices[0]
    distances, suggestions = model.kneighbors(
        book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=5
    )
    return suggestions
class BookRecommendation(BaseModel):
    book_name: str  

@app.post("/recommend/")
async def get_recommendation(book: BookRecommendation):
    logger.info(f"Received request for book: {book.book_name}")

    try:
        suggestions = recommend_books(book.book_name, book_pivot, model, books_name_lower)
        book_details = fetch_book_details(suggestions, book_pivot, final_rating)
        return {"recommendations": book_details}
    except HTTPException as ve:
        logger.error(f"HTTPException: {str(ve)}")
        raise ve 
    except Exception as e:
        logger.error(f"Error during recommendation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
    
@app.get('/healthz')
def health():
    return 'OK'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run(app_import_string, host=HOST, port=PORT, reload=True)