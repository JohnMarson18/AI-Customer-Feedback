# Requisitos — AI Customer Feedback Analyzer

## Objetivo
App web gratuito que recebe vários feedbacks de clientes e devolve sentimento geral, resumo executivo e tópicos, usando Gemini (tier gratuito).

## Requisitos Funcionais
| ID | Requisito | Critério de aceite |
|----|-----------|--------------------|
| RF01 | Sidebar com campo de API key (senha) e instruções do Google AI Studio | Campo mascarado; link funcional; lê `GEMINI_API_KEY` do `.env` como padrão |
| RF02 | `st.text_area` para colar feedbacks + botão "Analisar Feedbacks" | Botão com texto vazio mostra erro amigável, sem chamar a API |
| RF03 | Sentimento geral (Positivo/Neutro/Negativo) + confiança 0–100 | Exibido com `st.metric` |
| RF04 | Resumo executivo em exatamente 3 bullets | Sempre 3 itens, em português |
| RF05 | Tópicos/tags recorrentes (3–8) | Exibidos como badges |
| RF06 | Botão "Carregar exemplo" | Preenche a text_area com dados de demonstração |
| RF07 | Contador de feedbacks analisados | `st.metric` |

## Requisitos Não Funcionais
- RNF01: Custo zero (Gemini free tier, Streamlit Community Cloud opcional).
- RNF02: Python 3.10+; apenas as 4 dependências do `requirements.txt`.
- RNF03: Chave nunca commitada nem logada; `.env` no `.gitignore`.
- RNF04: Erros (chave inválida, 429, 5xx, rede, resposta inválida) viram mensagens amigáveis via `AnalyzerError`; nunca stack trace na tela.
- RNF05: Entrada limitada a 30.000 caracteres.
- RNF06: Saída da IA em JSON estruturado validado por Pydantic.
- RNF07: Proteção básica contra prompt injection (feedbacks tratados como dados).

## Fora de escopo (backlog)
Upload CSV, gráficos por tópico, histórico, exportar PDF, testes automatizados com mock do cliente.

## Contrato entre módulos
```python
# analyzer.py
analyze_feedbacks(api_key: str, feedbacks: str) -> FeedbackAnalysis   # levanta AnalyzerError
count_feedbacks(text: str) -> int
class FeedbackAnalysis(BaseModel):
    sentimento_geral: Literal["Positivo","Neutro","Negativo"]
    confianca: int            # 0-100
    justificativa: str
    resumo_executivo: list[str]   # 3 itens
    topicos: list[str]
```
