"""Agente de IA simples, no terminal, usando o Ollama e ferramentas."""
import ollama

import ferramentas

MODELO = "qwen2.5:3b"
SISTEMA = (
    "Você é um assistente prestativo. Responda sempre em português do Brasil. "
    "Use as ferramentas quando o pedido envolver hora, tarefas ou arquivos."
)


def conversar() -> None:
    historico = [{"role": "system", "content": SISTEMA}]
    print("Agente pronto. Digite 'sair' para encerrar.")
    while True:
        texto = input("Você: ").strip()
        if texto.lower() in ("sair", "exit"):
            break
        if not texto:
            continue
        historico.append({"role": "user", "content": texto})
        while True:
            resposta = ollama.chat(
                model=MODELO,
                messages=historico,
                tools=list(ferramentas.TODAS.values()),
            )
            mensagem = resposta.message
            historico.append(mensagem)
            if not mensagem.tool_calls:
                print(f"Agente: {mensagem.content}")
                break
            for chamada in mensagem.tool_calls:
                nome = chamada.function.name
                resultado = ferramentas.executar(nome, chamada.function.arguments)
                historico.append(
                    {"role": "tool", "content": resultado, "tool_name": nome}
                )


if __name__ == "__main__":
    conversar()
