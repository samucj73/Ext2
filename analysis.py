
from collections import Counter

VERMELHOS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
PRETOS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

def analisar_estatisticas(history):
    numeros = [item["number"] for item in history]
    lucky = sum((item["lucky_numbers"] for item in history), [])

    freq = Counter(numeros)
    lucky_freq = Counter(lucky)
    hot = freq.most_common(5)
    cold = freq.most_common()[-5:]

    vermelhos = [n for n in numeros if n in VERMELHOS]
    pretos = [n for n in numeros if n in PRETOS]
    baixos = [n for n in numeros if 1 <= n <= 18]
    altos = [n for n in numeros if 19 <= n <= 36]

    return {
        "🔥 Números Quentes": [f"{n} ({c}x)" for n, c in hot],
        "❄️ Números Frios": [f"{n} ({c}x)" for n, c in cold],
        "⚡ Lucky Numbers Frequentes": [f"{n} ({c}x)" for n, c in lucky_freq.most_common(5)],
        "🎨 Vermelhos": [str(n) for n in vermelhos],
        "🖤 Pretos": [str(n) for n in pretos],
        "🔻 Baixos (1-18)": [str(n) for n in baixos],
        "🔺 Altos (19-36)": [str(n) for n in altos]
    }
