import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# === Load data ===
df = pd.read_csv("../data/player_game_prediction_matrix.csv", index_col="Player")

# === Fill missing values ===
filled_df = df.fillna(0)

# === Compute cosine similarity ===
similarity_matrix = cosine_similarity(filled_df)

# Create DataFrame with proper labels
similarity_df = pd.DataFrame(similarity_matrix, index=filled_df.index, columns=filled_df.index)
similarity_df = similarity_df.round(2)

# === Show top 5 most similar players for each ===
top_matches = {}

for player in similarity_df.index:
    # Drop self and sort by similarity
    top_others = similarity_df.loc[player].drop(player).sort_values(ascending=False).head(5)
    top_matches[player] = top_others

# === Save to CSV for exploration ===
top_matches_df = pd.DataFrame(top_matches).T
top_matches_df.to_csv("../output/top_5_similar_players.csv")

similarity_df.to_csv("../output/player_similarity_matrix.csv")
print("📈 Full player similarity matrix saved to output/player_similarity_matrix.csv")


print("✅ Top 5 compatible players saved to output/top_5_similar_players.csv")
