import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === Load similarity matrix ===
df = pd.read_csv("../output/player_similarity_matrix.csv", index_col=0)

# === Create heatmap ===
plt.figure(figsize=(10, 8))
sns.heatmap(df, annot=True, cmap="YlGnBu", square=True, linewidths=0.5, vmin=0, vmax=1, cbar_kws={"label": "Similarity (0 to 1)"})

plt.title("🎯 Player Taste Similarity Heatmap", fontsize=16)
plt.tight_layout()

# === Save to file ===
plt.savefig("../output/player_similarity_heatmap.png", dpi=300)
plt.show()
