import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.get(url, params={"chat_id": chat_id, "text": message})
    except Exception as e:
        print(f"Telegram error: {e}")

def check_fac():
    fac = [
        "https://www.fac-habitat.com/fr/residences-etudiantes/id-57-philosophia",
        "https://www.fac-habitat.com/fr/residences-etudiantes/id-46-belle-isle",
        # Add more URLs here...
    ]
    for url in fac:
        try:
            html = requests.get(url).text
            iframe = html.split('iframe class="reservation" width="100%" height="150" src="')[1].split('"')[0]
            iframe_content = requests.get(iframe).text
            if "D&eacute;poser une demande" in iframe_content:
                send_telegram(f"Found spot at: {url}")
        except Exception as e:
            print(f"Error: {e}")

def check_crous():
    url = "https://trouverunlogement.lescrous.fr/tools/36/search?maxPrice=600&occupationModes=alone&bounds=2.224122_48.902156_2.4697602_48.8155755"
    content = requests.get(url).text
    if "Aucun logement trouv" not in content and "Serveur satur" not in content:
        send_telegram("Crous alert! Room found:\n" + url)

if __name__ == "__main__":
    check_fac()
    check_crous()
