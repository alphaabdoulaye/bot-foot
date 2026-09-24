from flask import Flask, render_template_string, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyseur Foot Pro & Statistiques</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 15px; margin: 0; }
        h1 { font-size: 1.3rem; color: #38bdf8; text-align: center; margin-bottom: 15px; }
        .match-card { background: #1e293b; padding: 12px; margin-bottom: 12px; border-radius: 10px; border-left: 4px solid #38bdf8; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .teams { font-weight: bold; font-size: 1rem; margin-bottom: 6px; }
        .badge { display: inline-block; background: #0284c7; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; margin-right: 4px; margin-bottom: 4px; }
        .badge-btts { background: #d97706; }
        .badge-market { background: #059669; }
        .details { font-size: 0.85rem; color: #94a3b8; margin-top: 6px; line-height: 1.3; }
    </style>
</head>
<body>
    <h1>⚽ Analyseur Marchés & Matchs</h1>
    <div id="matches">Chargement et analyse des matchs en cours...</div>

    <script>
        fetch('/api/matches')
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById('matches');
                if (data.length === 0) {
                    container.innerHTML = "<p style='text-align:center;'>Aucun match disponible pour le moment.</p>";
                    return;
                }
                container.innerHTML = data.map(m => `
                    <div class="match-card">
                        <div class="teams">${m.home} vs ${m.away}</div>
                        <div>
                            <span class="badge badge-btts">BTTS: ${m.btts}</span>
                            <span class="badge badge-market">Marché: ${m.market}</span>
                            <span class="badge">xG Fav: ${m.xg_fav}</span>
                        </div>
                        <div class="details">💡 <b>Analyse :</b> ${m.analysis}</div>
                    </div>
                `).join('');
            });
    </script>
</body>
</html>
"""

def analyze_match_criteria(home, away, has_schedule_congestion, defensive_fragility, high_stakes, ref_tolerance):
    """
    Moteur d'analyse basé sur vos critères exacts :
    - BTTS, xG du favori, fragilité défensive.
    - Impact d'un calendrier chargé (baisse xG favori, hausse fragilité, boost BTTS).
    - Enjeux, rivalités et facteur arbitre.
    """
    btts_score = "Non"
    market = "Victoire Favori (Clean Sheet)"
    xg_fav = "Haut (~1.8)"
    notes = []

    # Règle calendrier chargé / milieu de semaine
    if has_schedule_congestion:
        xg_fav = "Diminué (~1.2)"
        defensive_fragility = True # S'accentue
        btts_score = "Oui (Fortement probable)"
        notes.append("Calendrier chargé : efficacité xG du favori en baisse, fragilité défensive accentuée.")
    
    # Règle fragilité défensive & BTTS
    if defensive_fragility:
        btts_score = "Oui"
        market = "BTTS & Over 2.5"
        notes.append("Fragilité défensive détectée chez l'adversaire ou le favori.")

    # Règle enjeux et rivalités
    if high_stakes:
        notes.append("Match à fort enjeu / rivalité : tension accrue.")
        if ref_tolerance == "Strict":
            notes.append("Arbitre strict : attention aux cartons et penalties potentiels.")
        else:
            notes.append("Arbitre tolérant : duels physiques favorisés.")

    analysis_text = " | ".join(notes) if notes else "Rencontre équilibrée selon les standards statistiques."

    return {
        "home": home,
        "away": away,
        "btts": btts_score,
        "market": market,
        "xg_fav": xG_fav,
        "analysis": analysis_text
    }

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/matches')
def api_matches():
    # Ici, vous pourrez brancher un vrai scraping de matchs du jour (ex: depuis des pages publiques)
    # Pour l'instant, on simule l'injection de matchs en direct analysés par votre algorithme :
    
    match_1 = analyze_match_criteria(
        home="Manchester City", away="Arsenal", 
        has_schedule_congestion=True, 
        defensive_fragility=True, 
        high_stakes=True, 
        ref_tolerance="Strict"
    )
    
    match_2 = analyze_match_criteria(
        home="Real Madrid", away="Real Sociedad", 
        has_schedule_congestion=False, 
        defensive_fragility=False, 
        high_stakes=True, 
        ref_tolerance="Modéré"
    )

    return jsonify([match_1, match_2])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
