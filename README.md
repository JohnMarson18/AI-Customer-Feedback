# 📊 AI Customer Feedback Analyzer

> Transforme múltiplos feedbacks de clientes em insights claros (sentimento, tópicos e resumo executivo) em segundos, utilizando inteligência artificial com custo zero.

---

## ✨ O que o app faz

Ao colar comentários, reviews ou mensagens de clientes, a aplicação processa o lote e retorna:
- **Sentimento Geral**: Positivo, Neutro ou Negativo com porcentagem de confiança.
- **Resumo Executivo**: Exatamente 3 pontos acionáveis baseados exclusivamente nos feedbacks.
- **Principais Tópicos**: Tags dos assuntos mais citados (ex: entrega, atendimento, preço).
- **Contador Automático**: Total de feedbacks identificados e analisados no lote.

---

## 🚀 Como Executar em 3 Passos

### 1. Clonar e preparar o ambiente
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configurar a API Key do Gemini (Gratuita)
Obtenha sua chave gratuita no [Google AI Studio](https://aistudio.google.com/apikey).

Crie o arquivo `.env` a partir do exemplo:
```bash
# Windows:
copy .env.example .env
# Linux/Mac:
cp .env.example .env
```
Abra o `.env` e cole sua chave:
```env
GEMINI_API_KEY=sua_chave_aqui
```
*(Você também pode digitar ou colar a chave diretamente na barra lateral da aplicação)*.

### 3. Rodar a aplicação
```bash
streamlit run app.py
```

---

## 🤖 Construído com Inteligência Artificial

Este projeto foi totalmente planejado, desenvolvido, testado e documentado de forma autônoma por um **escritório colaborativo de agentes de IA** utilizando o framework **Munder Difflin** e **Google Antigravity**.

A divisão de trabalho e os modelos utilizados por cada agente foram:

| Agente | Papel | Responsabilidade | Modelo de IA Utilizado |
|---|---|---|---|
| **Michael Scott** | Orquestrador | Arquitetura, governança, kanban e integração Git | **Gemini 3.8 Flash (High)** |
| **Dwight Schrute** | Backend / IA | Prompt engineering, schemas Pydantic e chamadas ao Gemini | **Gemini 3.8 Flash (Medium)** |
| **Pam Beesly** | Frontend / UI | Interface Streamlit, sidebar, métricas visuais e badges | **Gemini 3.8 Flash (Medium)** |
| **Jim Halpert** | Docs & QA | Gestão de dependências, `.gitignore` seguro e testes automatizados | **Gemini 3.8 Flash (Medium)** |

### Modelo de IA da Aplicação
Para processar os feedbacks dos clientes em tempo de execução, o app consome a API oficial do Google através do pacote `google-genai`:
- **Modelo**: `gemini-2.5-flash` (tier gratuito do Google AI Studio).
- **Segurança**: Saída estruturada estrita via Pydantic (`response_schema`) e isolamento dos feedbacks em `<feedbacks>` para mitigação de prompt injection.

---

## 📄 Licença
Distribuído sob a licença MIT.
