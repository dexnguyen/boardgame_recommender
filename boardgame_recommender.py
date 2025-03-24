import pandas as pd

# Load a sample dataset (you can replace with real BGG data later)
data ={
    "Game": ["Catan", "Ticket to Ride", "Pandemic", "Codenames", "Agricola"],
    "Strategy": [3, 2, 2, 1, 3],
    "Bluffing": [1, 1, 1, 2, 1],
    "Complexity": [2, 1, 2, 1, 3]
}

df = pd.DataFrame(data)

# Find the game with the highest strategy rating
best_strategy_game = df.loc[df["Strategy"].idxmax()]

print("Best strategy game recommendation:", best_strategy_game["Game"])