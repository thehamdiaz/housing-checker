import os
import requests

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHANNEL_CHAT_ID")
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

def check_crous_Tours():
    url = "https://trouverunlogement.lescrous.fr/tools/41/search?occupationModes=alone&bounds=0.2885071238975235_48.10559716402152_1.8238464793662736_46.74550709985597"
    content = requests.get(url).text
    if "Aucun logement trouv" not in content and "Serveur satur" not in content:
        send_telegram("Crous Tours alert! Room found:\n" + url)

def check_crous_IDF():
    url = "https://trouverunlogement.lescrous.fr/tools/41/search?occupationModes=alone&bounds=1.524108116042711_49.384160800744986_3.0594474715114615_48.057889555610984"
    content = requests.get(url).text
    if "Aucun logement trouv" not in content and "Serveur satur" not in content:
        send_telegram("Crous IDF alert! Room found:\n" + url)

if __name__ == "__main__":
    check_fac()
    check_crous_Tours()
    check_crous_IDF()
