import pandas as pd

# Load the full recommendation matrix
df = pd.read_csv("top_100_recommendation_matrix.csv")

# Melt into long format (Player, Game, Score)
melted = df.melt(id_vars=["Player"], var_name="Game", value_name="Score")

# Drop 0 scores (optional: only recommend games they might like)
filtered = melted[melted["Score"] > 0]

# Sort and get top 5 per player
top_5 = (
    filtered
    .sort_values(["Player", "Score"], ascending=[True, False])
    .groupby("Player")
    .head(5)
)

# Save to CSV
top_5.to_csv("top_5_recommendations.csv", index=False)
print("✅ Top 5 game recommendations per player saved to 'top_5_recommendations.csv'")
