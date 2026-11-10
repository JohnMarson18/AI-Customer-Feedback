"""Interface Streamlit. Toda a lógica de IA vive em analyzer.py."""
import os

import streamlit as st
from dotenv import load_dotenv

from analyzer import MAX_CHARS, AnalyzerError, analyze_feedbacks, count_feedbacks

load_dotenv()

st.set_page_config(page_title="AI Customer Feedback Analyzer", page_icon="📊", layout="wide")

SAMPLE = """Chegou muito rápido e bem embalado, adorei!

O atendimento demorou 3 dias para responder meu e-mail. Decepcionante.

Produto bom, mas achei caro perto da concorrência.

Suporte resolveu meu problema em minutos, nota 10.

A entrega atrasou uma semana e ninguém avisou."""

SENTIMENT_EMOJI = {"Positivo": "😊", "Neutro": "😐", "Negativo": "😟"}

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🔑 Configuração")
    api_key = st.text_input(
        "GEMINI_API_KEY",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Usada apenas nesta sessão; não é armazenada.",
    )
    st.markdown(
        """
**Como obter grátis:**
1. Acesse [Google AI Studio](https://aistudio.google.com/apikey)
2. Entre com sua conta Google
3. Clique em **Create API key**
4. Cole a chave acima

O tier gratuito é suficiente para este projeto.
"""
    )

# ---------- Main ----------
st.title("📊 AI Customer Feedback Analyzer")
st.caption("Cole vários feedbacks de clientes e receba sentimento, resumo executivo e tópicos com Gemini.")

if "texto" not in st.session_state:
    st.session_state["texto"] = ""

if st.button("📋 Carregar exemplo"):
    st.session_state["texto"] = SAMPLE

texto = st.text_area(
    "Feedbacks dos clientes",
    key="texto",
    height=250,
    placeholder="Cole aqui os reviews, um por linha ou separados por linha em branco...",
    max_chars=MAX_CHARS,
)

if st.button("🔍 Analisar Feedbacks", type="primary"):
    if not api_key or not api_key.strip():
        st.error("Informe sua GEMINI_API_KEY na barra lateral.")
    elif not texto or not texto.strip():
        st.error("Cole pelo menos um feedback para analisar.")
    else:
        try:
            with st.spinner("Analisando com Gemini..."):
                result = analyze_feedbacks(api_key, texto)
        except AnalyzerError as err:
            st.error(str(err))
        except Exception:
            st.error("Ocorreu um erro inesperado ao processar os feedbacks. Tente novamente.")
        else:
            st.divider()
            c1, c2, c3 = st.columns(3)
            emoji = SENTIMENT_EMOJI.get(result.sentimento_geral, "📊")
            c1.metric("Sentimento Geral", f"{emoji} {result.sentimento_geral}")
            c2.metric("Confiança", f"{result.confianca}%")
            c3.metric("Feedbacks analisados", count_feedbacks(texto))
            if result.justificativa:
                st.caption(result.justificativa)

            st.divider()
            st.subheader("📝 Resumo Executivo")
            for point in result.resumo_executivo:
                st.markdown(f"- {point}")

            st.divider()
            st.subheader("🏷️ Principais Tópicos")
            if result.topicos:
                st.markdown(" ".join(f":blue-badge[{t}]" for t in result.topicos))
            else:
                st.info("Nenhum tópico identificado.")
