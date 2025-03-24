import pandas as pd
from collections import Counter

# Load the owned games dataset
df = pd.read_csv("owned_games.csv")

# Extract all categories and mechanics
all_categories = []
all_mechanics = []

for categories in df["categories"].dropna():
    all_categories.extend(categories.split(", "))

for mechanics in df["mechanics"].dropna():
    all_mechanics.extend(mechanics.split(", "))

# Count occurrences of each
category_counts = Counter(all_categories)
mechanic_counts = Counter(all_mechanics)

# Get the top 10 most common ones
top_categories = category_counts.most_common(10)
top_mechanics = mechanic_counts.most_common(10)

# Print results
print("\n🔹 **Top 10 Most Common Categories:**")
for cat, count in top_categories:
    print(f"{cat}: {count}")

print("\n🔹 **Top 10 Most Common Mechanics:**")
for mech, count in top_mechanics:
    print(f"{mech}: {count}")

# Save to CSV for reference
df_top = pd.DataFrame(top_categories, columns=["Category", "Count"])
df_top.to_csv("top_categories.csv", index=False)

df_mech = pd.DataFrame(top_mechanics, columns=["Mechanic", "Count"])
df_mech.to_csv("top_mechanics.csv", index=False)

print("\n✅ Data saved to top_categories.csv & top_mechanics.csv!")
