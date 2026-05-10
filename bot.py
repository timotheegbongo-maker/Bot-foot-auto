import os
import requests
from groq import Groq

# 1. Configuration des clés (récupérées depuis les secrets GitHub)
FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")

def get_football_scores():
    # Exemple : Récupère les matchs en direct (Live)
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {'x-apisports-key': FOOTBALL_API_KEY}
    response = requests.get(url, headers=headers).json()
    
    if response['results'] > 0:
        match = response['response'][0] # On prend le premier match en live
        equipe_h = match['teams']['home']['name']
        equipe_a = match['teams']['away']['name']
        score_h = match['goals']['home']
        score_a = match['goals']['away']
        return f"{equipe_h} {score_h} - {score_a} {equipe_a}"
    return None

def generate_ai_post(score_text):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"Agis comme un journaliste sportif passionné. Rédige un post Facebook court et percutant pour annoncer ce score en direct : {score_text}. Utilise des emojis."
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def post_to_facebook(message):
    url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
    payload = {'message': message, 'access_token': FB_ACCESS_TOKEN}
    r = requests.post(url, data=payload)
    return r.json()

# Exécution du robot
score = get_football_scores()
if score:
    texte_ia = generate_ai_post(score)
    resultat = post_to_facebook(texte_ia)
    print("Post publié avec succès !")
else:
    print("Pas de match en cours pour le moment.")
