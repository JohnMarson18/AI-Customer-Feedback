# Customer Feedback Analyzer

Aplicação web em Streamlit para análise automática de feedbacks de clientes utilizando a API do Google Gemini.

## Funcionalidades
- Classificação de sentimento geral (Positivo, Neutro ou Negativo) com nível de confiança.
- Resumo executivo em 3 pontos objetivos.
- Identificação de tópicos recorrentes.
- Gráficos de distribuição de sentimentos e tópicos.
- Upload de arquivos `.csv` e `.txt` (com seleção de coluna para planilhas).
- Exportação dos relatórios em Markdown (.md) e dados em CSV (.csv).

## Pré-requisitos
- Python 3.10+
- Chave de API do Gemini (gratuita no [Google AI Studio](https://aistudio.google.com/apikey))

## Instalação e Execução

1. Clone o repositório e crie o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure a chave de API:
Copie o arquivo de exemplo:
```bash
cp .env.example .env  # No Windows: copy .env.example .env
```
Edite o arquivo `.env`:
```env
GEMINI_API_KEY=sua_chave_aqui
```
*(A chave também pode ser informada diretamente na barra lateral da aplicação).*

4. Inicie o app:
```bash
streamlit run app.py
```

## Arquitetura
- `app.py`: Interface Streamlit, uploads, gráficos e downloads.
- `analyzer.py`: Chamadas ao Gemini via SDK `google-genai`, schema Pydantic, parsers e exportações.
- `sample_feedbacks.csv`: Base de dados de exemplo para testes de importação.

## Modelos Utilizados
- Inferência da aplicação: Gemini 2.5 Flash (`gemini-2.5-flash`).
- Desenvolvimento assistido por IA: Gemini 3.8 Flash (High/Medium) via framework multiagente.

## Licença
MIT
