from flask import Flask, request, render_template
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load dataset with error handling
try:
    trending_products = pd.read_csv("models/trending_products.csv")
    train_data = pd.read_csv("models/clean_data.csv")

    # Ensure required columns exist
    required_columns = {"Name", "Tags", "ReviewCount", "Brand", "ImageURL", "Rating"}
    if not required_columns.issubset(train_data.columns):
        print("Error: Required columns missing in clean_data.csv")
        train_data = pd.DataFrame()  # Reset if incorrect

except FileNotFoundError as e:
    print(f"Error: {e}")
    trending_products = pd.DataFrame()
    train_data = pd.DataFrame()

# Fill NaN values in 'Tags' column
if not train_data.empty and "Tags" in train_data.columns:
    train_data['Tags'] = train_data['Tags'].fillna('')

# Function to truncate text for display
def truncate(text, length):
    return text[:length] + "..." if len(text) > length else text

# Content-based recommendation function
def content_based_recommendations(train_data, item_name, top_n=10):
    if train_data.empty:
        print("Error: Dataset is empty.")
        return pd.DataFrame(columns=['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating'])

    # Make a temporary copy to avoid modifying the original DataFrame
    temp_df = train_data.copy()
    temp_df['Name'] = temp_df['Name'].str.lower()
    item_name = item_name.lower().strip()

    if item_name not in temp_df['Name'].values:
        print(f"Product '{item_name}' not found in dataset.")
        return pd.DataFrame(columns=['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating'])

    # TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(temp_df['Tags'])

    # Compute cosine similarity
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # Get index of searched product
    item_index = temp_df[temp_df['Name'] == item_name].index[0]

    # Find similar items
    similar_items = sorted(enumerate(cosine_similarities_content[item_index]), key=lambda x: x[1], reverse=True)
    top_similar_items = similar_items[1:top_n+1]
    recommended_item_indices = [x[0] for x in top_similar_items]

    return train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]

# Routes
random_image_urls = [
    "static/image/img_1.png", "static/image/img_2.png", "static/image/img_3.png", 
    "static/image/img_4.png", "static/image/img_5.png", "static/image/img_6.png", 
    "static/image/img_7.png", "static/image/img_8.png"
]

@app.route("/")
def index():
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))

@app.route("/main")
def main():
    return render_template('main.html', content_based_rec=pd.DataFrame(), message="Search for a product.")

@app.route("/recommendations", methods=['POST'])
def recommendations():
    prod = request.form.get('prod', '').strip()
    nbr = request.form.get('nbr', '').strip()

    # Debugging: Print input values
    print(f"Received product: {prod}")
    print(f"Number of recommendations requested: {nbr}")

    if not prod:
        return render_template('recommendations.html', content_based_rec=pd.DataFrame(), message="Please enter a product name.")

    if not nbr.isdigit():
        return render_template('recommendations.html', content_based_rec=pd.DataFrame(), message="Please enter a valid number.")

    nbr = int(nbr)

    content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

    if content_based_rec.empty:
        return render_template('recommendations.html', content_based_rec=content_based_rec, message=f"No recommendations found for '{prod}'.")

    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(content_based_rec))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]

    return render_template('recommendations.html', content_based_rec=content_based_rec, truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))

if __name__ == '__main__':
    app.run(debug=True)
