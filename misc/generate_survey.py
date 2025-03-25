import pandas as pd
import re

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "", filename)

# Load your game list
df = pd.read_csv("owned_games.csv")

# Base HTML scaffold
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Board Game Survey</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { padding: 2rem; }
    .game-card { margin-bottom: 2rem; display: flex; gap: 1rem; align-items: flex-start; }
    .game-img { width: 120px; height: auto; border-radius: 8px; object-fit: cover; }
    textarea { resize: vertical; }
  </style>
</head>
<body>
  <h2 class="mb-4">Board Game Preference Survey</h2>

  <form id="survey-form">
    <div class="mb-4">
      <label for="player_name" class="form-label">Player Name</label>
      <input type="text" class="form-control" name="player_name" required>
    </div>

    <!-- GAME_CARDS_HERE -->

    <button type="button" class="btn btn-primary mt-4" onclick="downloadCSV()">Download My Answers (CSV)</button>
  </form>

  <script>
    function downloadCSV() {
      const form = document.getElementById('survey-form');
      const formData = new FormData(form);
      const playerName = formData.get('player_name');
      if (!playerName) {
        alert('Please enter your name!');
        return;
      }

      let csv = "Player,Game ID,Game Name,Rating,Comment\\n";

      const games = [...new Set(Array.from(formData.keys()).map(k => k.split('__')[0]).filter(k => k !== 'player_name'))];
      games.forEach(id => {
        const rating = formData.get(id + '__rating') || '';
        const comment = (formData.get(id + '__comment') || '').replace(/\\n/g, ' ').replace(/,/g, ';');
        const name = document.getElementById(id + '__title').innerText;
        csv += `${playerName},${id},"${name}",${rating},"${comment}"\\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `survey_${playerName}.csv`;
      link.click();
    }
  </script>
</body>
</html>
"""

# Build game cards
game_cards_html = ""
for _, row in df.iterrows():
    game_id = str(row["id"])
    game_name = row["name"]
    sanitized_name = sanitize_filename(game_name)
    image_path = f"data/{sanitized_name}_thumbnail.jpg"

    card = f"""
    <div class="game-card">
      <img src="{image_path}" alt="{game_name}" class="game-img">
      <div>
        <h5 id="{game_id}__title">{game_name}</h5>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="{game_id}__rating" value="-2" id="{game_id}_hate">
          <label class="form-check-label" for="{game_id}_hate">Hate (-2)</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="{game_id}__rating" value="-1" id="{game_id}_dislike">
          <label class="form-check-label" for="{game_id}_dislike">Don’t like (-1)</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="{game_id}__rating" value="0" id="{game_id}_neutral">
          <label class="form-check-label" for="{game_id}_neutral">It’s ok (0)</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="{game_id}__rating" value="1" id="{game_id}_like">
          <label class="form-check-label" for="{game_id}_like">Like (+1)</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="{game_id}__rating" value="2" id="{game_id}_love">
          <label class="form-check-label" for="{game_id}_love">Love (+2)</label>
        </div>
        <div class="form-check mt-2">
          <input class="form-check-input" type="radio" name="{game_id}__rating" value="N/A" id="{game_id}_not_played">
          <label class="form-check-label" for="{game_id}_not_played">Haven’t played yet</label>
        </div>
        <div class="mt-2">
          <label for="{game_id}__comment" class="form-label">Comments:</label>
          <textarea class="form-control" name="{game_id}__comment" rows="2" placeholder="Why do you love/hate this game? (optional)"></textarea>
        </div>
      </div>
    </div>
    """
    game_cards_html += card

# Inject into template
final_html = html_template.replace("<!-- GAME_CARDS_HERE -->", game_cards_html)

# Save file
with open("player_survey.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("✅ Survey generated as 'player_survey.html'")
