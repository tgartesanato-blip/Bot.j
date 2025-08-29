# th_ia.py
# TH IA - Assistente de Estudos, Programação e Correção de Códigos

import sys
import textwrap
from dataclasses import dataclass
from typing import List

INTENTS = [
    {
        "nome": "saudacao",
        "padroes": ["oi", "olá", "e aí", "bom dia", "boa tarde"],
        "respostas": ["Olá! Eu sou a TH IA 🤖. Posso explicar, gerar ou corrigir códigos para você!"]
    },
    {
        "nome": "despedida",
        "padroes": ["tchau", "até mais", "falou", "valeu"],
        "respostas": ["Até mais! Continue estudando e praticando programação. 💻"]
    },
    {
        "nome": "ajuda",
        "padroes": ["ajuda", "como usar", "o que você faz"],
        "respostas": [
            "Eu sou a TH IA. Posso:\n"
            "- Explicar conceitos de programação\n"
            "- Criar códigos sob pedido (ex.: 'faça um programa de fatorial')\n"
            "- Avaliar e corrigir códigos que você colar aqui"
        ]
    },
]

# ----------------- 1) Mini-base de conhecimento -----------------
BASE_CONCEITOS = {
    "listas python": """Em Python, listas são coleções mutáveis:
```python
frutas = ["maçã", "banana", "uva"]
frutas.append("laranja")
print(frutas[0])  # acessa o primeiro elemento
```""",
    "for python": """O `for` em Python:
```python
for i in range(5):
    print(i)
```""",
    "algoritmo": "Um algoritmo é uma sequência de passos lógicos para resolver um problema."
}

# ----------------- 2) Gerador de código -----------------
def gerar_codigo(pedido: str) -> str:
    pedido = pedido.lower()

    if "fatorial" in pedido:
        return textwrap.dedent("""\
        Aqui está um programa em Python que calcula o fatorial de um número:
        ```python
        def fatorial(n):
            if n == 0 or n == 1:
                return 1
            return n * fatorial(n-1)

        num = int(input("Digite um número: "))
        print("Fatorial:", fatorial(num))
        ```
        """)
    elif "ordenar" in pedido:
        return textwrap.dedent("""\
        Programa em Python que ordena uma lista de números:
        ```python
        numeros = [5, 2, 9, 1, 7]
        numeros.sort()
        print("Lista ordenada:", numeros)
        ```
        """)
    else:
        return "Ainda não sei gerar esse código específico, mas posso te ajudar a escrever passo a passo. 😉"

# ----------------- 3) Avaliador de código -----------------
def avaliar_codigo(codigo: str) -> str:
    """Analisa e tenta corrigir código Python colado pelo usuário."""
    try:
        compile(codigo, "<string>", "exec")
        return "✅ Seu código parece correto! Talvez dê para melhorar com boas práticas.\n" \
               "Exemplo: usar funções para organizar melhor."
    except SyntaxError as e:
        return f"❌ Encontrei um erro de sintaxe na linha {e.lineno}: {e.text}\n" \
               f"Sugestão: verifique parênteses, dois pontos e indentação."
    except Exception as e:
        return f"⚠️ Seu código executa, mas encontrei um possível problema: {e}\n" \
               f"Sugestão: revise a lógica."

# ----------------- 4) Classificação -----------------
def classificar(texto: str) -> str:
    texto = texto.lower().strip()

    # check intents fixas
    for intent in INTENTS:
        for p in intent["padroes"]:
            if p in texto:
                return intent["nome"]

    # se pedir código
    if any(p in texto for p in ["faça", "programa", "crie", "escreva código", "gerar código"]):
        return "gerar_codigo"

    # se parece ser código (presença de "def", "print", "for", etc.)
    if any(p in texto for p in ["def ", "print", "for ", "while ", "class ", "import "]):
        return "avaliar_codigo"

    # conceitos
    for chave in BASE_CONCEITOS:
        if chave in texto:
            return "conceito"

    return "desconhecido"

# ----------------- 5) Núcleo da IA -----------------
@dataclass
class THIA:
    def responder(self, texto_usuario: str) -> str:
        categoria = classificar(texto_usuario)

        if categoria == "gerar_codigo":
            return gerar_codigo(texto_usuario)

        if categoria == "conceito":
            for chave, resposta in BASE_CONCEITOS.items():
                if chave in texto_usuario.lower():
                    return resposta

        if categoria == "avaliar_codigo":
            return avaliar_codigo(texto_usuario)

        for intent in INTENTS:
            if categoria == intent["nome"]:
                return intent["respostas"][0]

        return "Não entendi direito 🤔. Tente perguntar sobre programação, pedir um código ou colar um para eu avaliar."

# ----------------- 6) Loop do chat -----------------
def main():
    print("TH IA — Assistente de Estudos, Programação e Correção de Códigos. Digite 'sair' para encerrar.")
    bot = THIA()

    while True:
        try:
            texto = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTH IA: Até a próxima! 👋")
            break

        if texto.lower() in {"sair", "exit", "quit"}:
            print("TH IA: Até logo e bons estudos! 📚")
            break

        resposta = bot.responder(texto)
        print(f"TH IA: {resposta}")

if __name__ == "__main__":
    if sys.version_info < (3, 8):
        print("Use Python 3.8+")
        sys.exit(1)
    main()