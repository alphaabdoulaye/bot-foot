import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Clé API Football-Data
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "934b6fce2a73484791292a5d7318a83b")

# Liste des compétitions majeures
LEAGUE_CODES = {
    "Ligue 1": "FL1",
    "Premier League": "PL",
    "La Liga": "PD",
    "Serie A": "SA",
    "Bundesliga": "BL1",
    "Champions League": "CL"
}

headers = {
    "X-Auth-Token": FOOTBALL_DATA_API_KEY
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_matches", methods=["POST", "GET"])
def get_matches():
    """Récupère automatiquement les prochains matchs de tous les grands championnats."""
    all_matches = []
    
    for league_name, code in LEAGUE_CODES.items():
        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                matches_data = res.json().get("matches", [])
                for m in matches_data[:2]:  # Récupère 2 matchs par championnat
                    all_matches.append({
                        "league": league_name,
                        "team_a": m["homeTeam"]["name"],
                        "team_b": m["awayTeam"]["name"],
                        "date": m["utcDate"]
                    })
        except Exception as e:
            print(f"Erreur pour {league_name}: {e}")
            continue

    return jsonify({"status": "success", "matches": all_matches})

@app.route("/analyze_match", methods=["POST"])
def analyze_match():
    """Analyse automatique des deux équipes d'un match."""
    data = request.get_json() or {}
    team_a = data.get("team_a", "")
    team_b = data.get("team_b", "")
    league_name = data.get("league", "Premier League")

    code = LEAGUE_CODES.get(league_name, "PL")
    url_standings = f"https://api.football-data.org/v4/competitions/{code}/standings"
    
    try:
        res = requests.get(url_standings, headers=headers, timeout=10)
        standings_info = "Données non disponibles."
        
        if res.status_code == 200:
            tables = res.json().get("standings", [])
            if tables:
                table = tables[0].get("table", [])
                lines = []
                for team in table:
                    t_name = team["team"]["name"]
                    if team_a.lower() in t_name.lower() or team_b.lower() in t_name.lower():
                        lines.append(
                            f"Pos {team['position']}: {t_name} | Pts: {team['points']} | J: {team['playedGames']} | Diff: {team['goalDifference']} | Forme: {team.get('form', 'N/A')}"
                        )
                if lines:
                    standings_info = "\n".join(lines)

        return jsonify({
            "status": "success",
            "match": f"{team_a} vs {team_b}",
            "analysis": {
                "standings_raw": standings_info,
                "recent_form_raw": "Consultez les détails de forme dans le classement ci-dessus.",
                "h2h_raw": f"Compétition : {league_name}"
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
