"""Interface Streamlit. Toda a lógica de IA e processamento vive em analyzer.py."""
import os

import streamlit as st
from dotenv import load_dotenv

from analyzer import (
    MAX_CHARS,
    AnalyzerError,
    analyze_feedbacks,
    compute_chart_metrics,
    count_feedbacks,
    generate_csv_export,
    generate_markdown_report,
    get_csv_columns,
    parse_feedback_file,
)

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
    st.divider()
    st.caption("Desenvolvido de forma autônoma por um time multiagente (Michael, Dwight, Pam e Jim).")

# ---------- Main ----------
st.title("📊 AI Customer Feedback Analyzer")
st.caption("Receba sentimento geral, gráficos, resumo executivo e tópicos de feedbacks com Gemini 2.5 Flash.")

if "texto" not in st.session_state:
    st.session_state["texto"] = ""

# Botão de carregar exemplo (antes do widget text_area)
c_sample, c_info = st.columns([1, 4])
if c_sample.button("📋 Carregar exemplo"):
    st.session_state["texto"] = SAMPLE

# Seção de upload de arquivos (antes do widget text_area)
with st.expander("📂 Importar planilha ou arquivo de texto (.csv, .txt)", expanded=False):
    uploaded_file = st.file_uploader(
        "Selecione um arquivo .csv ou .txt contendo comentários de clientes:",
        type=["csv", "txt"],
        help="Limite de até 500 feedbacks ou 30.000 caracteres.",
    )
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        col_selected = None
        if uploaded_file.name.lower().endswith(".csv"):
            cols = get_csv_columns(file_bytes)
            if len(cols) > 1:
                col_selected = st.selectbox(
                    "Selecione a coluna que contém os feedbacks:",
                    cols,
                    help="Escolha qual campo da planilha contém o texto dos comentários.",
                )
        if st.button("📥 Importar feedbacks do arquivo"):
            try:
                extracted = parse_feedback_file(file_bytes, uploaded_file.name, col_selected)
                st.session_state["texto"] = "\n\n".join(extracted)
                st.success(f"{len(extracted)} feedbacks importados com sucesso de {uploaded_file.name}!")
            except AnalyzerError as err:
                st.error(str(err))

texto = st.text_area(
    "Feedbacks dos clientes",
    key="texto",
    height=230,
    placeholder="Cole aqui os reviews dos clientes (um por linha ou separados por linha em branco) ou suba um arquivo acima...",
    max_chars=MAX_CHARS,
)

if st.button("🔍 Analisar Feedbacks", type="primary"):
    if not api_key or not api_key.strip():
        st.error("Informe sua GEMINI_API_KEY na barra lateral.")
    elif not texto or not texto.strip():
        st.error("Cole pelo menos um feedback ou importe um arquivo para analisar.")
    else:
        try:
            with st.spinner("Analisando feedbacks com Gemini 2.5 Flash..."):
                result = analyze_feedbacks(api_key, texto)
        except AnalyzerError as err:
            st.error(str(err))
        except Exception:
            st.error("Ocorreu um erro inesperado ao conectar com o Gemini. Tente novamente.")
        else:
            total_count = count_feedbacks(texto)

            # --- Métricas Principais ---
            st.divider()
            c1, c2, c3 = st.columns(3)
            emoji = SENTIMENT_EMOJI.get(result.sentimento_geral, "📊")
            c1.metric("Sentimento Geral", f"{emoji} {result.sentimento_geral}")
            c2.metric("Confiança da IA", f"{result.confianca}%")
            c3.metric("Feedbacks analisados", total_count)
            if result.justificativa:
                st.caption(f"**Justificativa**: {result.justificativa}")

            # --- Gráficos Visuais (Etapa 2) ---
            st.divider()
            st.subheader("📊 Visualizações Gráficas")
            chart_metrics = compute_chart_metrics(result)
            g1, g2 = st.columns(2)
            with g1:
                st.caption("**Distribuição Estimada de Sentimento (%)**")
                st.bar_chart(chart_metrics["sentimentos"])
            with g2:
                st.caption("**Relevância dos Tópicos Identificados**")
                st.bar_chart(chart_metrics["topicos"])

            # --- Resumo Executivo ---
            st.divider()
            st.subheader("📝 Resumo Executivo")
            for point in result.resumo_executivo:
                st.markdown(f"- {point}")

            # --- Tópicos Recorrentes ---
            st.divider()
            st.subheader("🏷️ Principais Tópicos")
            if result.topicos:
                st.markdown(" ".join(f":blue-badge[{t}]" for t in result.topicos))
            else:
                st.info("Nenhum tópico identificado.")

            # --- Exportação de Relatórios (Etapa 3) ---
            st.divider()
            st.subheader("📥 Exportar Resultados")
            exp1, exp2 = st.columns(2)

            md_report = generate_markdown_report(result, total_count)
            exp1.download_button(
                label="📄 Baixar Relatório Executivo (.md)",
                data=md_report,
                file_name="relatorio_feedbacks.md",
                mime="text/markdown",
                help="Download do relatório executivo completo em formato Markdown.",
            )

            csv_report = generate_csv_export(result)
            exp2.download_button(
                label="📊 Baixar Dados Consolidados (.csv)",
                data=csv_report.encode("utf-8-sig"),
                file_name="analise_feedbacks.csv",
                mime="text/csv",
                help="Download compatível com Microsoft Excel (Windows) com acentuação corrigida.",
            )
