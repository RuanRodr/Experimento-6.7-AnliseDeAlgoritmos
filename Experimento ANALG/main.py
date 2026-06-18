import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.set_int_max_str_digits(1000000)

def gerar_numero(digitos):
    primeiro = str(random.randint(1, 9))
    resto = ''.join(str(random.randint(0, 9)) for _ in range(digitos - 1))
    return int(primeiro + resto)

def multiplicacao_direta(x, y):
    return x * y

def divisao_conquista(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2
    p = 10 ** m

    a, b = x // p, x % p
    c, d = y // p, y % p

    ac = divisao_conquista(a, c)
    ad = divisao_conquista(a, d)
    bc = divisao_conquista(b, c)
    bd = divisao_conquista(b, d)

    return ac * (10 ** (2 * m)) + (ad + bc) * p + bd

def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2
    p = 10 ** m

    a, b = x // p, x % p
    c, d = y // p, y % p

    z0 = karatsuba(b, d)
    z2 = karatsuba(a, c)
    z1 = karatsuba(a + b, c + d) - z0 - z2

    return z2 * (10 ** (2 * m)) + z1 * p + z0

def medir_tempo(funcao, a, b):
    inicio = time.perf_counter()
    funcao(a, b)
    fim = time.perf_counter()
    return fim - inicio

print("=" * 50)
print("VALIDAÇÃO DOS ALGORITMOS")
print("=" * 50)

a_teste = 4234
b_teste = 6231

r1 = multiplicacao_direta(a_teste, b_teste)
r2 = divisao_conquista(a_teste, b_teste)
r3 = karatsuba(a_teste, b_teste)

print(f"A = {a_teste}")
print(f"B = {b_teste}")
print(f"Direta = {r1}")
print(f"Divisão e Conquista = {r2}")
print(f"Karatsuba = {r3}")
print(f"Resultados iguais? {r1 == r2 == r3}")
print()

tamanhos = [100, 500, 1000, 2000, 5000]

resultados = []

for n in tamanhos:
    tempos_direta = []
    tempos_dc = []
    tempos_karatsuba = []

    for _ in range(10):
        a = gerar_numero(n)
        b = gerar_numero(n)

        r1 = multiplicacao_direta(a, b)
        r2 = divisao_conquista(a, b)
        r3 = karatsuba(a, b)

        assert r1 == r2 == r3

        tempos_direta.append(medir_tempo(multiplicacao_direta, a, b))
        tempos_dc.append(medir_tempo(divisao_conquista, a, b))
        tempos_karatsuba.append(medir_tempo(karatsuba, a, b))

    resultados.append({
        "digitos": n,
        "direta": sum(tempos_direta)/10,
        "div_conq": sum(tempos_dc)/10,
        "karatsuba": sum(tempos_karatsuba)/10
    })

df = pd.DataFrame(resultados)
print(df)

plt.figure(figsize=(10, 6))

plt.plot(
    df["digitos"],
    df["direta"],
    marker="o",
    label="Direta"
)

plt.plot(
    df["digitos"],
    df["div_conq"],
    marker="o",
    label="Divisão e Conquista"
)

plt.plot(
    df["digitos"],
    df["karatsuba"],
    marker="o",
    label="Karatsuba"
)

plt.xlabel("Quantidade de Dígitos")
plt.ylabel("Tempo Médio (s)")
plt.title("Comparação dos Algoritmos")

plt.grid(True)
plt.legend()

plt.savefig("grafico.png")
plt.show()                