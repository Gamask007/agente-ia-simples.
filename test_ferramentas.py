import tempfile
import unittest
from pathlib import Path

import ferramentas


class TestFerramentas(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        base = Path(self.pasta.name)
        ferramentas.ARQUIVO_TAREFAS = base / "tarefas.json"
        ferramentas.PASTA_BASE = base

    def tearDown(self):
        self.pasta.cleanup()

    def test_hora_atual_tem_formato_de_data_e_hora(self):
        self.assertRegex(ferramentas.hora_atual(), r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$")

    def test_lista_vazia(self):
        self.assertEqual(ferramentas.listar_tarefas(), "Nenhuma tarefa anotada.")

    def test_anotar_e_listar(self):
        ferramentas.anotar_tarefa("estudar GitHub")
        self.assertIn("1. [ ] estudar GitHub", ferramentas.listar_tarefas())

    def test_anotar_vazia_da_erro(self):
        self.assertTrue(ferramentas.anotar_tarefa("   ").startswith("Erro"))

    def test_concluir_tarefa(self):
        ferramentas.anotar_tarefa("fazer pull request")
        ferramentas.concluir_tarefa(1)
        self.assertIn("1. [x] fazer pull request", ferramentas.listar_tarefas())

    def test_concluir_tarefa_inexistente(self):
        self.assertTrue(ferramentas.concluir_tarefa(5).startswith("Erro"))

    def test_listar_pasta(self):
        (ferramentas.PASTA_BASE / "arquivo.txt").write_text("oi")
        self.assertIn("arquivo.txt", ferramentas.listar_pasta("."))

    def test_listar_pasta_fora_do_projeto_e_bloqueada(self):
        self.assertIn("acesso negado", ferramentas.listar_pasta(".."))

    def test_executar_ferramenta_desconhecida(self):
        self.assertTrue(ferramentas.executar("apagar_tudo", {}).startswith("Erro"))

    def test_executar_com_argumentos(self):
        resultado = ferramentas.executar("anotar_tarefa", {"descricao": "teste"})
        self.assertIn("anotada", resultado)


if __name__ == "__main__":
    unittest.main()
