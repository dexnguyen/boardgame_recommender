import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# === 1. Load rating matrix ===
ratings = pd.read_csv("../data/player_game_rating_matrix.csv", index_col="Player")

# === 2. Fill NaNs with 0 for similarity calc only
ratings_filled = ratings.fillna(0)

# === 3. Compute similarity matrix
similarity = cosine_similarity(ratings_filled)
similarity_df = pd.DataFrame(similarity, index=ratings.index, columns=ratings.index)

# === 4. Predict missing ratings ===
predicted_ratings = ratings.copy()

for player in ratings.index:
    for game in ratings.columns:
        if pd.isna(ratings.loc[player, game]):
            # Get all other players who rated this game
            other_players = ratings[ratings[game].notna()].index.tolist()
            if not other_players:
                predicted_ratings.loc[player, game] = 0
                continue

            # Similarity scores with current player
            sims = similarity_df.loc[player, other_players]
            # Ratings from those similar players
            ratings_for_game = ratings.loc[other_players, game]

            # Weighted average
            numerator = np.dot(sims, ratings_for_game)
            denominator = sims.sum()

            predicted_score = numerator / denominator if denominator != 0 else 0
            predicted_ratings.loc[player, game] = predicted_score

# === 5. Save predicted matrix ===
predicted_ratings.to_csv("../data/player_game_prediction_matrix.csv")
print("✅ Predicted ratings saved to 'player_game_prediction_matrix.csv'")
