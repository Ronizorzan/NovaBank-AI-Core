# NovaBank AI-Core: Assistente Inteligente de Atendimento (RAG Pro)

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688.svg)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-rgby)
![LGPD](https://img.shields.io/badge/LGPD-Compliance__Layer-green.svg)

O **NovaBank AI-Core** é uma solução de inteligência artificial generativa de ponta, desenvolvida para revolucionar o atendimento ao cliente do NovaBank. Este chatbot não apenas responde a perguntas, mas orquestra um fluxo complexo de segurança, eficiência e contextualização para entregar respostas precisas, rápidas e seguras.

A aplicação utiliza a arquitetura **RAG (Retrieval-Augmented Generation)**, potencializada por uma camada intermediária de **Cache Semântico (FAQ)** e uma camada de **Proteção de Dados Sensíveis (PII)**.

```
## 📊 Métricas de Sucesso da Aplicação

| Métrica | Sem AI-Core | Com AI-Core | Impacto Business |
|---|---|---|---|
| Tempo de Resposta (Média) | ~10-15 s (Humano) | < 2 s (TTFT via RAG) <br> < 100 ms (FAQ) | Aumento drástico na satisfação do cliente (CSAT) |
| Custo por Atendimento | Alto (Fator Humano) | Baixo (Tokens RAG) <br> Zero (Tokens FAQ) | Redução significativa no OPEX do Call Center |
| Taxa de Resolução (FCR) | Depende do treinamento | Alta e Consistente (Baseada na Doc.) | Menor reabertura de chamados |
| Risco de Vazamento de Dados | Humano/Processo | Mitigado via Software (Redação PII) | Conformidade LGPD e proteção da marca |
```

## 🌟 Proposta de Valor e Impacto no Negócio

Este projeto foi desenhado focando nos desafios reais de instituições financeiras modernas:

### 1. Experiência do Cliente (CX) Superior
* **Respostas Contextualizadas:** Utiliza a documentação interna real do banco para responder, garantindo acuracidade.
* **Latência Percebida Mínima:** Implementação de **Streaming de Resposta**, onde o usuário vê a resposta sendo construída em tempo real, eliminando a ansiedade da espera.

### 2. Eficiência Operacional e Redução de Custo (ROI)
* **Camada de Cache Semântico (FAQ):** Perguntas frequentes são resolvidas instantaneamente via busca vetorial em milissegundos, **sem custo de tokens de LLM** e sem latência de geração.
* **Métricas de Performance:** A API monitora o tempo médio de resposta, permitindo auditorias de eficiência.

### 3. Segurança e Conformidade (LGPD)
* **Redação de PII:** Uma camada de segurança inspeciona a pergunta do usuário e mascara dados sensíveis (CPF, Cartões, E-mails) *antes* que eles sejam enviados para modelos de IA externos, garantindo conformidade com a LGPD.

---

## 🛠️ Arquitetura Técnica e Fluxo de Dados

A aplicação expõe um endpoint de streaming assíncrono (`api/v1/query-stream`) que orquestra o seguinte fluxo:

graph TD
    User[Usuário] -->|Pergunta| API[FastAPI Endpoint]
    API -->|Sanitização| PII[Redação PII]
    PII -->|Pergunta Segura| FAQ[Cache Semântico (ChromaDB)]
    
    FAQ -->|Match Forte (>Threshold)| Stream[Streaming de Resposta]
    FAQ -->|Sem Match| RAG[Pipeline RAG]
    
    RAG -->|Busca Vetorial| Docs[Documentação Interna (ChromaDB)]
    Docs -->|Contexto| LLM[OpenAI GPT-4o-mini]
    LLM -->|Tokens Gerados| Stream
    
    Stream -->|Eventos SSE| User



## 📁 Estrutura do Projeto
```
project/
├── .env                    # Para adicionar as chaves de API
├── chroma_db_faq           # Banco de dados vetorial do FAQ
├── files/                  # PDFs utilizados no sistema RAG
├── data/                   # Dados  de FAQ que vão alimentar o sistema (quanto mais completo, melhor)
│   └── faq.py              # O arquivo FAQ de perguntas e respostas prontas (dados puros)
├── functions_src/          # Módulo de funções e classes principais
│   ├── faq_engine.py       # Lógica para criar/gerenciar o banco de FAQ
│   ├── rag_pipeline.py     # Pipeline de documentos (centraliza o pipeline dos documentos RAG)
│   └── security.py         # Segurança dos dados (Verificação e anonimização de dados sigilosos)
└── app.py                  # Aplicação FastAPI (centralizada somente a lógica principal da API)
└── Dockerfile              # Arquivo de conteinerização (para deploy rápido e eficiente)
```
