import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Load predicted matrix ===
df = pd.read_csv("../data/player_game_prediction_matrix.csv", index_col="Player")

# === 2. Create heatmap ===
plt.figure(figsize=(len(df.columns) * 0.5 + 5, len(df.index) * 0.6 + 3))
sns.heatmap(df, cmap="coolwarm", center=0, linewidths=0.5, annot=False)

# === 3. Customize ===
plt.title("🎯 Predicted Player Preferences (Collaborative Filtering)")
plt.xlabel("Games")
plt.ylabel("Players")
plt.xticks(rotation=90)
plt.tight_layout()

# === 4. Save and show ===
plt.savefig("predicted_rating_heatmap.png")
plt.show()

print("✅ Heatmap saved as 'predicted_rating_heatmap.png'")
