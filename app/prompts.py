REFORMED_MUSIC_INFO_EXTRACTION_PROMPT = """
A seguir, você verá a letra e cifra de uma música cristã. Sua tarefa é analisar o texto com base na perspectiva cristã reformada e responder preenchendo um JSON estruturado com as informações solicitadas, conforme o exemplo fornecido.

Aqui está a estrutura de saída esperada (JSON) com cada campo e uma breve descrição:

{{
  "titulo": "<Título da música>",
  "autor": "<Nome do(s) autor(es) da música>",
  "album": "<Nome do álbum em que a música foi lançada>",
  "ano": "<Ano de lançamento>",
  "resumo": "<Resumo objetivo da mensagem central da música>",
  "referencias_biblicas": [
    {{
      "versiculo": "<Referência bíblica associada ao conteúdo da música (ex: Salmo 145:3)>",
      "contexto": "<Contexto ou explicação breve da passagem e sua relação com a música>"
    }},
    ...
  ],
  "explicacao_teologica": "<Explicação teológica sobre a letra, enfatizando a perspectiva reformada, como soberania divina, cristocentricidade ou outras doutrinas principais>",
  "correcoes_teologicas": {{
    "possui_inconsistencias": <true ou false - indica se a música possui erros teológicos>,
    "observacoes": "<Descrição de erros ou inconsistências teológicas, se houver>"
  }},
  "aplicabilidade_congregacional": "<Sugestões de uso da música (ex: culto de adoração, célula, reunião de jovens)>",
  "classificacoes": {{
    "precisao_biblica": <Classificação de 1 a 5 - avalia a precisão com que a letra reflete a Bíblia>,
    "cristocentricidade": <Classificação de 1 a 5 - avalia o quanto a música foca em Cristo como o centro da mensagem>",
    "adequacao_congregacional": <Classificação de 1 a 5 - indica quão adequada é a música para uso em congregação>",
    "profundidade_teologica": <Classificação de 1 a 5 - avalia a complexidade e profundidade teológica da letra>,
    "coerencia_doutrinaria": <Classificação de 1 a 5 - avalia a consistência doutrinária da música com a teologia reformada>"
  }},
  "tags": ["<Lista de palavras-chave para temas abordados na música, como adoração, soberania de Deus, graça, etc.>"],
  "conexao_confessional": {{
    "confissao_de_fe": "<Capítulo e Artigo da Confissão de Fé de Westminster, se aplicável>",
    "catecismo_maior": [
      {{
        "pergunta": "<Número da pergunta>",
        "resumo": "<Explicação resumida sobre como a letra reflete o conteúdo da pergunta do catecismo>"
      }}
    ]
  }},
  "exegese_detalhada": [
    {{
      "trecho": "<Trecho específico da letra>",
      "analise": "<Análise teológica ou doutrinária do trecho, explicando seu significado>"
    }},
    ...
  ],
  "estrutura_musical": {{
    "tempo": "<Tempo da música (ex: 4/4)>",
    "tom": "<Tom musical da música (ex: Dó maior)>",
    "dificuldade": "<Nível de dificuldade para execução (ex: baixa, média, alta)>",
    "observacoes": "<Observações sobre a estrutura musical e adequação para congregação>"
  }},
  "recomendacao_liturgica": "<Sugestão de momentos litúrgicos para uso da música (ex: abertura de culto, adoração coletiva)>",
  "sensibilidade_cultural": {{
    "relevancia": "<Nível de relevância cultural para diferentes contextos (ex: alta, média, baixa)>",
    "contexto": "<Descrição do contexto cultural ou localidade em que a música é mais adequada>"
  }}
}}

### Letra e Cifra da Música:
{music_sheet}

---

Após revisar a letra e a cifra acima, responda preenchendo o JSON conforme a estrutura especificada, com uma análise fiel ao conteúdo da música e sua adequação à perspectiva reformada.
"""
