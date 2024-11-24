REFORMED_MUSIC_INFO_EXTRACTION_PROMPT = """
A seguir, você verá a letra e cifra de uma música, que pode ser cristã ou não. 
Sua tarefa é analisar o texto com rigor teológico baseado na perspectiva \
reformada e responder preenchendo um JSON estruturado com as informações \
 solicitadas. Não deve haver flexibilização, interpretação vaga ou \
 relativização dos temas fundamentais da fé reformada.

Para músicas não cristãs ou que contenham heresias ou inconsistências \
teológicas, a análise deve ser crítica e direta, evidenciando as falhas com \
clareza. Por exemplo, músicas com heresias como: "Sou meu próprio guia", 
"O poder está dentro de mim", ou "Somos deuses" devem ser avaliadas de forma a\
 sublinhar suas contradições com a fé cristã e seu desvio das doutrinas \
 reformadas.

Para músicas cristãs que apresentem inconsistências, falta de profundidade ou 
conteúdo raso, o agente deve aplicar rigor, sem suavizar a análise ou "forçar" 
uma interpretação coerente. Cada erro ou ponto problemático deve ser \
evidenciado objetivamente.

Aqui está a estrutura de saída esperada (JSON) com cada campo e uma \
breve descrição:

{{
  "titulo": "<Título da música>",
  "autor": "<Nome do(s) autor(es) da música>",
  "album": "<Nome do álbum em que a música foi lançada>",
  "ano": "<Ano de lançamento>",
  "resumo": "<Resumo objetivo da mensagem central da música>",
  "referencias_biblicas": [
    {{
      "versiculo": "<Referência bíblica associada ao conteúdo da música (ex: \
      Salmo 145:3)>",
      "contexto": "<Contexto ou explicação breve da passagem e sua relação com\
       a música>"
    }},
    ...
  ],
  "explicacao_teologica": "<Explicação teológica sobre a letra, enfatizando a \
  perspectiva reformada, incluindo soberania divina, cristocentricidade, e \
  doutrinas centrais>",
  "correcoes_teologicas": {{
    "possui_inconsistencias": <true ou false - indica se a música possui erros\
     teológicos>,
    "observacoes": "<Descrição de erros ou inconsistências teológicas, se\
     houver, de forma clara e sem relativizações>"
  }},
  "aplicabilidade_congregacional": "<Sugestões de uso da música (ex: culto \
  de adoração, célula, reunião de jovens)>",
  "classificacoes": {{
    "precisao_biblica": <Classificação de 1 a 5 - avalia a precisão com que \
    a letra reflete a Bíblia>,
    "cristocentricidade": <Classificação de 1 a 5 - avalia o quanto a música \
    foca em Cristo como o centro da mensagem>",
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

Após revisar a letra e a cifra acima, responda preenchendo o JSON conforme a estrutura especificada, com uma análise fiel e rígida ao conteúdo da música, destacando claramente falhas doutrinárias ou teológicas onde encontradas.
"""
