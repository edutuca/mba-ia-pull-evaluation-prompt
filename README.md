# Técnicas Aplicadas — Bug to User Story (v2)

Documentação das técnicas de prompt engineering usadas para refatorar o prompt de conversão de relatos de bugs em User Stories.

O prompt otimizado está em [prompts/bug_to_user_story_v2.yml](prompts/bug_to_user_story_v2.yml). Ele combina cinco técnicas: o Few-shot Learning é obrigatório; as demais são complementares.

## Sumário

- [1. Role Prompting](#1-role-prompting)
- [2. Chain of Thought (CoT)](#2-chain-of-thought-cot)
- [3. Skeleton of Thought](#3-skeleton-of-thought)
- [4. Tree of Thought (versão leve)](#4-tree-of-thought-versão-leve)
- [5. Few-shot Learning](#5-few-shot-learning)
- [Edge cases tratados](#edge-cases-tratados)
- [Técnicas não utilizadas](#técnicas-não-utilizadas)

## 1. Role Prompting

**O que é:** definir uma persona e o contexto de atuação do modelo.

**Por que foi escolhida:** o v1 não definia quem estava escrevendo. Sem persona, o modelo tende a produzir textos genéricos, sem o vocabulário e o rigor de um Product Owner. Definir o papel orienta o tom, o nível de detalhe e a preocupação com critérios testáveis.

**Como foi aplicada:** o `system_prompt` começa com "Você é um Product Owner sênior com experiência em QA, requisitos ágeis e escrita de User Stories", deixando explícito que a saída é em português do Brasil.

## 2. Chain of Thought (CoT)

**O que é:** instruir o modelo a raciocinar em etapas antes de responder.

**Por que foi escolhida:** classificar um bug, separar sintoma de comportamento esperado e extrair dados concretos (IDs, endpoints, códigos HTTP) são tarefas que se beneficiam de uma análise intermediária. Sem ela, o modelo costuma pular direto para a escrita e perde detalhes do relato.

**Como foi aplicada:** o system prompt lista cinco passos internos: classificar o tipo do problema, identificar o usuário afetado, separar sintoma de comportamento esperado, extrair dados concretos e avaliar a complexidade. Há a instrução explícita de **não exibir** esse raciocínio na saída, para que a avaliação receba apenas a User Story.

## 3. Skeleton of Thought

**O que é:** definir um esqueleto fixo de resposta, preenchido em etapas.

**Por que foi escolhida:** o dataset tem relatos de complexidades muito diferentes. Um bug de validação de email pede uma história curta; um checkout com quatro falhas críticas pede uma estrutura com seções. Um esqueleto por nível de complexidade torna a saída previsível e facilita a avaliação das métricas de clareza e completude.

**Como foi aplicada:** o prompt define dois esqueletos:

- **Simples/médio:** frase "Como..., eu quero..., para que...", seguida de "Critérios de Aceitação" em formato Dado/Quando/Então/E e, para bugs técnicos, um bloco "Contexto Técnico".
- **Complexo:** bloco "=== USER STORY PRINCIPAL ===" (título e descrição) e bloco "=== CRITÉRIOS DE ACEITAÇÃO ===" com seções lettered (A, B, C…), uma por problema independente.

## 4. Tree of Thought (versão leve)

**O que é:** explorar múltiplos caminhos de raciocínio e depois consolidar.

**Por que foi escolhida:** relatos complexos misturam problemas de natureza diferente (segurança, integração, lógica de negócio, UX). Tratá-los como um fluxo único faz o modelo abandonar algum deles. Tratar cada problema como um ramo independente garante cobertura de todos.

**Como foi aplicada:** a instrução pede que, em relatos com vários problemas, cada um seja avaliado isoladamente e depois consolidado em uma única User Story, com um bloco de critérios por ramo. Não foi implementada uma busca com avaliação de ramos em múltiplas chamadas, por custo e por não ser necessária para este dataset.

## 5. Few-shot Learning

**O que é:** fornecer exemplos de entrada e saída esperadas.

**Por que foi escolhida:** é a técnica obrigatória do desafio e a que mais influencia o formato da saída. Os exemplos mostram o estilo de escrita, o nível de detalhe e a diferença entre os três níveis de complexidade.

**Como foi aplicada:** o prompt inclui três exemplos extraídos de [datasets/bug_to_user_story.jsonl](datasets/bug_to_user_story.jsonl):

1. **Simples:** validação de email (sem "@").
2. **Médio:** webhook de pagamento retornando HTTP 500, com bloco "Contexto Técnico".
3. **Complexo:** checkout com múltiplas falhas (XSS no cupom, cobrança duplicada, limite de cupom e feedback de UX), condensado para manter o prompt de tamanho razoável.

**Limitação conhecida:** os exemplos vêm do mesmo dataset usado na avaliação. As notas obtidas podem, por isso, ser otimistas em relação a relatos inéditos. Um conjunto de validação separado seria a forma de medir a generalização.

## Edge cases tratados

- **Informação ausente:** o modelo usa placeholders entre colchetes (ex.: `[nome do gateway de pagamento]`) em vez de inventar dados.
- **Vários problemas no mesmo relato:** tratados como ramos separados (Tree of Thought), com critérios próprios.
- **Bugs de segurança:** exigem critérios de bloqueio/sanitização e de não vazamento de dados.
- **Bugs de performance:** exigem metas numéricas quando o relato as permite.
- **Regressão:** inclui critério de que o comportamento que já funciona continua funcionando.

## Técnicas não utilizadas

- **ReAct:** exige uso de ferramentas (busca, consulta a sistemas). A tarefa é uma transformação de texto sem acesso externo, então não há ação a executar.
- **Tree of Thought completo:** a versão leve atende ao requisito e evita o custo de múltiplas chamadas por relato.
