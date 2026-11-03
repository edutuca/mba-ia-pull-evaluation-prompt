"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

DICAS DE IMPLEMENTAÇÃO:

- O push é feito pelo cliente do LangSmith:

      from langsmith import Client
      from langchain_core.prompts import ChatPromptTemplate

      client = Client()
      prompt = ChatPromptTemplate.from_messages([
          ("system", system_prompt),
          ("user", user_prompt),
      ])
      url = client.push_prompt(
          f"{username}/bug_to_user_story_v2",
          object=prompt,
          is_public=True,
          description="...",
          tags=[...],
      )

- `username` vem de USERNAME_LANGSMITH_HUB no .env e precisa ser o seu handle
  do Hub. Se você ainda não tem um handle, veja as instruções no .env.example.

- A variável do template precisa ser {bug_report}, que é a chave de entrada
  usada no dataset de avaliação.

- Use `load_yaml` de utils.py para ler o arquivo .yml.
"""
import os
import yaml
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate

load_dotenv(dotenv_path='.env.example', override=True)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """



def main():
    with open("prompts/bug_to_user_story_v2.yml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)["bug_to_user_story_v2"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", data["system_prompt"]),
        ("user", data["user_prompt"]),
    ])

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    print(f"Username: {username}")
    if not username:
        print("USERNAME_LANGSMITH_HUB não definido no .env")
        return 1

    cliente = Client()
    url = cliente.push_prompt(
        f"{username}/bug_to_user_story_v2",
        object=prompt,
        is_public=True,
        description=data.get("description"),
        tags=data.get("tags"),
    )
    print(f"Prompt enviado: {url}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
