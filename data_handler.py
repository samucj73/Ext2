import requests
import csv
import os

API_URL = "https://api.casinoscores.com/svc-evolution-game-events/api/xxxtremelightningroulette/latest"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
ARQUIVO_CSV = "resultados.csv"

def fetch_latest_result():
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            game_data = data.get("data", {})
            result = game_data.get("result", {})
            outcome = result.get("outcome", {})
            lucky_list = result.get("luckyNumbersList", [])

            number = outcome.get("number")
            timestamp = game_data.get("startedAt")
            lucky_numbers = [item["number"] for item in lucky_list]

            return {
                "number": number,
                "timestamp": timestamp,
                "lucky_numbers": lucky_numbers
            }
    except:
        return None

def salvar_resultado_em_arquivo(result):
    if result is None:
        return

    # Cria o arquivo se não existir
    arquivo_existe = os.path.exists(ARQUIVO_CSV)
    with open(ARQUIVO_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if not arquivo_existe:
            writer.writerow(["timestamp", "number", "lucky_numbers"])
        writer.writerow([
            result["timestamp"],
            result["number"],
            "-".join(map(str, result["lucky_numbers"]))
        ])
