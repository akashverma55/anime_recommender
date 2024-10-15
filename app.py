from flask import Flask, render_template, request
import pickle
import pandas as pd

# Load the model from pickle file
anime = pickle.load(open("anime.pkl", "rb"))
anime_df = pd.DataFrame(anime)
anime_list = anime_df['Name'].values

theta = pickle.load(open("theta.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.form["anime_input"].lower() # Convert input to lowercase
    recommendations = predict_anime(user_input)  # Function to call the model
    recommendations = [sentence.capitalize() for sentence in recommendations]

    return render_template("recommendation.html", recommendations=recommendations)

def predict_anime(user_input):
    # Convert DataFrame 'Name' column to lowercase for comparison
    # anime_df['Name'] = anime_df['Name'].str.lower()
    
    # Check if the user input exists in the DataFrame
    if user_input not in anime_df['Name'].values:
        return ["No recommendations found. Please try another anime or genre."]
    
    # Get the index of the anime in the DataFrame
    anime_index = anime_df[anime_df["Name"] == user_input].index[0]
    
    # Get the similarity scores for the input anime
    distances = theta[anime_index]
    
    # Get the indices of the top 5 most similar animes (excluding the input anime itself)
    anime_list_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    # Generate the list of recommended anime titles
    recommended_anime_list = [anime_df.iloc[i[0]]['Name'] for i in anime_list_indices]

    return recommended_anime_list

if __name__ == '__main__':
    app.run(debug=True)
