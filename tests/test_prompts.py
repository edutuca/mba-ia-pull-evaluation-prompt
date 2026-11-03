"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="module")
def prompt_data():
    """Dados do bloco 'bug_to_user_story_v2' do arquivo de prompt."""
    return load_prompts(PROMPT_PATH)["bug_to_user_story_v2"]


@pytest.fixture(scope="module")
def system_prompt(prompt_data):
    return prompt_data.get("system_prompt", "")


class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        system_prompt = prompt_data.get("system_prompt")
        assert isinstance(system_prompt, str)
        assert system_prompt.strip(), "system_prompt está vazio"

    def test_prompt_has_role_definition(self, system_prompt):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        assert "Você é" in system_prompt

    def test_prompt_mentions_format(self, system_prompt):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        assert "Como " in system_prompt
        assert "Critérios de Aceitação" in system_prompt

    def test_prompt_has_few_shot_examples(self, system_prompt):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        assert system_prompt.count("Entrada:") >= 2
        assert system_prompt.count("Saída:") >= 2

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        text = prompt_data.get("system_prompt", "") + prompt_data.get("user_prompt", "")
        assert "TODO" not in text

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])
        assert len(techniques) >= 2, f"Encontradas apenas {len(techniques)} técnicas"

    def test_validate_prompt_structure(self, prompt_data):
        """Valida a estrutura geral do prompt com o utilitário do projeto."""
        is_valid, errors = validate_prompt_structure(prompt_data)
        assert is_valid, errors


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
