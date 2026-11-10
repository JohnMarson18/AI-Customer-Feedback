# AGENTS.md — Guia para agentes (Antigravity / Munder Difflin)

Leia `docs/REQUIREMENTS.md` ANTES de qualquer ação. O contrato de funções lá é a fonte da verdade.

## Papéis (execução paralela, sem sobreposição de arquivos)
| Agente | Dono dos arquivos | Entrega |
|--------|-------------------|---------|
| **Orquestrador** | `docs/`, `AGENTS.md` | Valida contrato, resolve conflitos, aprova entrega final |
| **Agente IA/Backend** | `analyzer.py` | Schema, prompt, chamada Gemini, tratamento de erros |
| **Agente UI** | `app.py` | Sidebar, text_area, resultados, mensagens de erro |
| **Agente Docs/QA** | `README.md`, `requirements.txt`, `.env.example`, `.gitignore` | Docs e checklist de QA abaixo |

Regra de ouro: **nunca edite arquivo de outro agente**. Precisa de mudança? Peça ao Orquestrador para alterar o contrato.

## Regras anti-erro
1. SDK correto: `from google import genai` (pacote `google-genai`). **Proibido** `google-generativeai` / `import google.generativeai`.
2. Modelo: `gemini-2.5-flash`. Constante única `MODEL_NAME` em `analyzer.py`.
3. `app.py` NÃO chama o Gemini diretamente; só usa `analyze_feedbacks`.
4. `analyzer.py` NÃO importa `streamlit`.
5. Sem dependências novas além de `requirements.txt`.
6. Nunca hardcode, logue ou imprima a API key. Nunca commitar `.env`.
7. Toda mensagem ao usuário em português do Brasil.
8. Não alterar assinaturas do contrato sem aprovação do Orquestrador.
9. Streamlit: não alterar `st.session_state["texto"]` depois que o widget com `key="texto"` foi criado (só em callbacks/botões antes dele).
10. Não use `st.badge`/`:blue-badge[]` com Streamlit < 1.44.

## Definition of Done (QA)
- [ ] `pip install -r requirements.txt` roda limpo em venv novo
- [ ] `streamlit run app.py` abre sem erros
- [ ] Sem chave → erro amigável; chave inválida → erro amigável
- [ ] Texto vazio → erro amigável, sem chamada à API
- [ ] "Carregar exemplo" + "Analisar" mostra: sentimento, confiança, contador, 3 bullets, tags
- [ ] README: passos de instalação testados do zero
- [ ] `git status` não mostra `.env`
