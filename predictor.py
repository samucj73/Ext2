
from collections import Counter

VERMELHOS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
PRETOS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

def prever_numeros_provaveis(caminho_arquivo='historico_resultados.txt', top_n=10):
    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()

        numeros = []
        for linha in linhas:
            partes = linha.strip().split('|')
            if len(partes) >= 2:
                try:
                    num = int(partes[0].strip())
                    numeros.append(num)
                except ValueError:
                    continue

        if not numeros:
            return []

        freq = Counter(numeros)

        pares = [n for n in numeros if n % 2 == 0]
        impares = [n for n in numeros if n % 2 != 0]
        vermelhos = [n for n in numeros if n in VERMELHOS]
        pretos = [n for n in numeros if n in PRETOS]
        baixos = [n for n in numeros if 1 <= n <= 18]
        altos = [n for n in numeros if 19 <= n <= 36]

        pontuacao = {}
        for n in range(0, 37):
            score = freq[n] * 1.2
            if n in vermelhos: score += 0.5
            if n in pretos: score += 0.5
            if n in baixos: score += 0.5
            if n in altos: score += 0.5
            score += 0.3  # peso neutro para todos

            pontuacao[n] = score

        provaveis = sorted(pontuacao.items(), key=lambda x: x[1], reverse=True)
        return [n for n, _ in provaveis[:top_n]]

    except Exception as e:
        print(f"[Erro na previsão]: {e}")
        return []
