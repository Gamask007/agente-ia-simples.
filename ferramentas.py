"""Ferramentas que o agente pode usar."""
import json
from datetime import datetime
from pathlib import Path

ARQUIVO_TAREFAS = Path("tarefas.json")
PASTA_BASE = Path(".")


def hora_atual() -> str:
    """Retorna a data e a hora atuais."""
    return datetime.now().strftime("%d/%m/%Y %H:%M")


def _carregar() -> list:
    if ARQUIVO_TAREFAS.exists():
        return json.loads(ARQUIVO_TAREFAS.read_text(encoding="utf-8"))
    return []


def _salvar(tarefas: list) -> None:
    texto = json.dumps(tarefas, ensure_ascii=False, indent=2)
    ARQUIVO_TAREFAS.write_text(texto, encoding="utf-8")


def anotar_tarefa(descricao: str) -> str:
    """Anota uma nova tarefa na lista.

    Args:
        descricao: o texto da tarefa a ser anotada.
    """
    descricao = descricao.strip()
    if not descricao:
        return "Erro: a descrição da tarefa está vazia."
    tarefas = _carregar()
    tarefas.append({"descricao": descricao, "feita": False})
    _salvar(tarefas)
    return f"Tarefa {len(tarefas)} anotada: {descricao}"


def listar_tarefas() -> str:
    """Mostra todas as tarefas anotadas, com o número de cada uma."""
    tarefas = _carregar()
    if not tarefas:
        return "Nenhuma tarefa anotada."
    linhas = []
    for numero, tarefa in enumerate(tarefas, start=1):
        marca = "x" if tarefa["feita"] else " "
        linhas.append(f"{numero}. [{marca}] {tarefa['descricao']}")
    return "\n".join(linhas)


def concluir_tarefa(numero: int) -> str:
    """Marca uma tarefa como concluída.

    Args:
        numero: o número da tarefa, como aparece na lista.
    """
    tarefas = _carregar()
    if not 1 <= numero <= len(tarefas):
        return f"Erro: a tarefa {numero} não existe."
    tarefas[numero - 1]["feita"] = True
    _salvar(tarefas)
    return f"Tarefa {numero} concluída: {tarefas[numero - 1]['descricao']}"


def listar_pasta(caminho: str = ".") -> str:
    """Lista os arquivos de uma pasta do projeto.

    Args:
        caminho: a pasta a listar, relativa à pasta do projeto.
    """
    base = PASTA_BASE.resolve()
    alvo = (base / caminho).resolve()
    if not alvo.is_relative_to(base):
        return "Erro: acesso negado, essa pasta fica fora do projeto."
    if not alvo.is_dir():
        return f"Erro: a pasta {caminho} não existe."
    nomes = sorted(item.name for item in alvo.iterdir())
    return "\n".join(nomes) if nomes else "A pasta está vazia."


TODAS = {
    funcao.__name__: funcao
    for funcao in (hora_atual, anotar_tarefa, listar_tarefas,
                   concluir_tarefa, listar_pasta)
}


def executar(nome: str, argumentos: dict) -> str:
    """Executa a ferramenta pedida pelo modelo e devolve o resultado."""
    if nome not in TODAS:
        return f"Erro: a ferramenta {nome} não existe."
    try:
        return str(TODAS[nome](**argumentos))
    except TypeError as erro:
        return f"Erro nos argumentos: {erro}"
