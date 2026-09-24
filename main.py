from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Template HTML intégré directement dans le fichier pour éviter de multiplier les dossiers
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyseur Foot Pro</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 15px; margin: 0; }
        h1 { font-size: 1.4rem; color: #38bdf8; text-align: center; margin-bottom: 20px; }
        .match-card { background: #1e293b; padding: 15px; margin-bottom: 12px; border-radius: 12px; border-left: 4px solid #38bdf8; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .teams { font-weight: bold; font-size: 1.1rem; margin-bottom: 8px; }
        .badge { display: inline-block; background: #0284c7; color: white; padding: 3px 8px; border-radius: 6px; font-size: 0.8rem; margin-right: 5px; }
        .details { font-size: 0.9rem; color: #94a3b8; margin-top: 6px; }
    </style>
</head>
<body>
    <h1>⚽ Analyseur & Prédictions Foot</h1>
    <div id="matches">Chargement des matchs et analyses...</div>

    <script>
        fetch('/api/matches')
            .then(res => res.json())
            .then(data => {
                const container = document.getElementById('matches');
                if (data.length === 0) {
                    container.innerHTML = "<p style='text-align:center;'>Aucun match pour le moment.</p>";
                    return;
                }
                container.innerHTML = data.map(m => `
                    <div class="match-card">
                        <div class="teams">${m.home} vs ${m.away}</div>
                        <div>
                            <span class="badge">BTTS: ${m.btts}</span>
                            <span class="badge" style="background: #059669;">Marché: ${m.market}</span>
                        </div>
                        <div class="details">💡 Analyse : ${m.notes}</div>
                    </div>
                `).join('');
            });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/matches')
def api_matches():
    # Exemple de données traitées selon vos critères (BTTS, fragilité défensive, calendrier chargé...)
    matches_fictifs = [
        {
            "home": "Équipe A", 
            "away": "Équipe B", 
            "btts": "Oui (Forte)", 
            "market": "BTTS & Over 2.5", 
            "notes": "Favori en milieu de semaine (calendrier chargé) -> xG ajusté à la baisse, fragilité défensive élevée."
        },
        {
            "home": "Équipe C", 
            "away": "Équipe D", 
            "btts": "Non", 
            "market": "Victoire Favori (Clean Sheet)", 
            "notes": "Solidité défensive solide, pas de match en semaine, gros enjeu de rivalité."
        }
    ]
    return jsonify(matches_fictifs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
