# app.py
# Checklist de Visita Técnica — Consultoria Mariner
# RDC 216 · Segurança dos Alimentos
# Streamlit application

import streamlit as st
from datetime import date, datetime
from modules.formulario import (
    SECOES,
    OPCOES_RESPOSTA,
    UNIDADES,
    Responsaveis,
    Nutricionistas,
    TOTAL_PERGUNTAS,
    TOTAL_PONTOS,
    calcular_pontuacao,
    classificar_nota,
)
from modules.dashboard import renderizar_dashboard
from modules.pdf_generator import gerar_pdf
from modules.whatsapp import gerar_link_whatsapp

# ──────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────────

st.set_page_config(
    page_title="Checklist Visita Técnica — Mariner",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────────
# CSS CUSTOMIZADO
# ──────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* Brand colors */
    :root {
        --gold: #C5A55A;
        --black: #1C1C1C;
        --grey: #666666;
        --light-grey: #F0EEEB;
        --white: #FAFAFA;
    }

    /* Brand header */
    .brand-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    .brand-header img {
        width: 120px;
        margin-bottom: 0.8rem;
    }
    .brand-header h1 {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.6rem;
        font-weight: 600;
        color: #1C1C1C;
        letter-spacing: 1px;
        margin: 0.5rem 0 0.2rem 0;
    }
    .brand-header .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #999;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
    }
    .gold-line {
        width: 60px;
        height: 2px;
        background: #C5A55A;
        margin: 0.8rem auto;
        border: none;
    }

    /* Section headers */
    .stSubheader, h2, h3 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #1C1C1C !important;
    }

    /* Separador dourado */
    .section-divider {
        border: none;
        border-top: 1.5px solid #C5A55A;
        margin: 1.5rem 0;
        opacity: 0.5;
    }

    /* TODAS as linhas hr do Streamlit em dourado */
    hr {
        border: none !important;
        border-top: 1.5px solid #C5A55A !important;
        opacity: 0.4;
    }

    /* Expanders com borda dourada */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        font-weight: 500;
    }
    details {
        border: 1px solid #E8DCC8 !important;
        border-radius: 8px !important;
    }
    details[open] {
        border-color: #C5A55A !important;
    }

    /* Tabs com acento dourado */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom-color: #C5A55A !important;
        color: #1C1C1C !important;
    }

    /* Botões com estilo gold */
    .stButton > button[kind="primary"] {
        background-color: #C5A55A !important;
        border-color: #C5A55A !important;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #B0913F !important;
        border-color: #B0913F !important;
    }

    /* Segmented control refinado */
    .stSegmentedControl {
        font-family: 'Inter', sans-serif;
    }

    /* Footer */
    .brand-footer {
        text-align: center;
        padding: 1rem 0;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #999;
        letter-spacing: 0.5px;
    }
    .brand-footer .gold-line {
        width: 40px;
        margin: 0.5rem auto;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# INICIALIZAR SESSION STATE
# ──────────────────────────────────────────────────

if "respostas" not in st.session_state:
    st.session_state.respostas = {}

if "observacoes" not in st.session_state:
    st.session_state.observacoes = {}

if "enviado" not in st.session_state:
    st.session_state.enviado = False


# ──────────────────────────────────────────────────
# HEADER COM LOGO DA MARCA
# ──────────────────────────────────────────────────

import base64
import os

logo_path = os.path.join("assets", "Logo-CC.PNG")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Caio Couto">'
else:
    logo_html = ""

st.markdown(f"""
<div class="brand-header">
    {logo_html}
    <h1>Checklist de Visita Tecnica</h1>
    <div class="gold-line"></div>
    <p class="subtitle">RDC 216 &middot; Seguranca dos Alimentos</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# INFORMAÇÕES DA VISITA
# ──────────────────────────────────────────────────

st.subheader("📋 Informações da Visita")

col1, col2 = st.columns(2)

with col1:
    unidade = st.selectbox(
        "Nome da Unidade",
        options=UNIDADES,
        help="Selecione o restaurante que está sendo visitado",
    )

with col2:
    data_visita = st.date_input(
        "Data da Visita",
        value=date.today(),
        format="DD/MM/YYYY",
        help="Data em que a visita técnica está sendo realizada",
    )


col3, col4 = st.columns(2)

with col3:
    responsavel = st.selectbox(
        "Responsável Técnico",
        options=Responsaveis,
        help="Nome completo do responsável técnico do restaurante",
    )

with col4:
    nutricionista = st.selectbox(
        "Nutricionista Avaliador",
        options=Nutricionistas,
        help="Nome completo do nutricionista que realiza a visita",
    )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# RENDERIZAÇÃO DAS SEÇÕES
# ──────────────────────────────────────────────────

st.subheader("📝 Avaliação por Seção")
st.caption(f"{len(SECOES)} seções · {TOTAL_PERGUNTAS} perguntas · {TOTAL_PONTOS} pontos possíveis")

for secao in SECOES:
    num = secao["numero"]
    titulo = secao["titulo"]
    pts_max = secao["pontuacao_maxima"]
    perguntas = secao["perguntas"]

    # Label simples — sem cálculo em tempo real para não fechar o expander
    label = f"{num}. {titulo}  ·  {len(perguntas)} perguntas  ·  {pts_max} pts"

    with st.expander(label, expanded=(num <= 3)):
        # Perguntas
        for pergunta in perguntas:
            pid = pergunta["id"]
            texto = pergunta["texto"]
            pontos = pergunta["pontos"]

            # Linha da pergunta com peso
            st.markdown(f"**{pid}** — {texto}  `({pontos} pts)`")

            # Segmented control — opções sem o "Selecione..."
            OPCOES_SEGMENTED = ["✅ Conforme", "❌ Não Conforme", "➖ N/A"]
            MAPA_SEGMENTED = {
                "✅ Conforme": "Conforme",
                "❌ Não Conforme": "Não Conforme",
                "➖ N/A": "Não Aplicável",
            }
            MAPA_REVERSO = {v: k for k, v in MAPA_SEGMENTED.items()}

            # Recuperar valor atual do session_state
            resp_atual = st.session_state.respostas.get(pid, None)
            default_val = MAPA_REVERSO.get(resp_atual, None)

            resposta_seg = st.segmented_control(
                "Conformidade",
                options=OPCOES_SEGMENTED,
                default=default_val,
                key=f"resp_{pid}",
                label_visibility="collapsed",
            )

            # Mapear de volta para o valor padrão do formulário
            if resposta_seg is not None:
                st.session_state.respostas[pid] = MAPA_SEGMENTED[resposta_seg]
            else:
                # Nenhuma opção selecionada ainda
                st.session_state.respostas[pid] = "Selecione..."

            # Observação inline
            obs_atual = st.session_state.observacoes.get(pid, "")
            obs = st.text_input(
                "Observação",
                value=obs_atual,
                placeholder="Observação (opcional)...",
                key=f"obs_{pid}",
                label_visibility="collapsed",
            )
            st.session_state.observacoes[pid] = obs

            st.markdown("---")

        # Observação geral da seção
        obs_secao_key = f"obs_secao_{num}"
        obs_secao_atual = st.session_state.observacoes.get(obs_secao_key, "")
        obs_secao = st.text_area(
            f"Observação geral — {titulo}",
            value=obs_secao_atual,
            placeholder="Observações adicionais sobre esta seção...",
            key=f"obs_geral_{num}",
            height=80,
        )
        st.session_state.observacoes[obs_secao_key] = obs_secao


st.markdown('<hr class="section-divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────────
# BOTÃO ENVIAR E FINALIZAR
# ──────────────────────────────────────────────────

st.subheader("✅ Finalizar Visita")

# Contar perguntas respondidas
total_respondidas = sum(
    1 for p_id, r in st.session_state.respostas.items()
    if r != "Selecione..."
)

# Validações
erros = []

if unidade == "Selecione a unidade...":
    erros.append("Selecione a unidade do restaurante")

if not responsavel.strip():
    erros.append("Preencha o nome do Responsável Técnico")

if not nutricionista.strip():
    erros.append("Preencha o nome do Nutricionista Avaliador")

perguntas_pendentes = TOTAL_PERGUNTAS - total_respondidas
if perguntas_pendentes > 0:
    erros.append(f"{perguntas_pendentes} perguntas ainda não respondidas")

# Mostrar avisos
if erros:
    for erro in erros:
        st.warning(f"⚠️ {erro}")

# Botão de envio
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    enviar = st.button(
        "📤  Enviar e Finalizar Relatório",
        type="primary",
        use_container_width=True,
        disabled=len(erros) > 0,
    )

if enviar and len(erros) == 0:
    st.session_state.enviado = True

    resultado = calcular_pontuacao(st.session_state.respostas)
    emoji, label_cls, cor = resultado["classificacao"]

    # Dados da visita para próximos módulos
    dados_visita = {
        "unidade": unidade,
        "data_visita": data_visita.strftime("%d/%m/%Y"),
        "responsavel": responsavel.strip(),
        "nutricionista": nutricionista.strip(),
        "resultado": resultado,
        "respostas": dict(st.session_state.respostas),
        "observacoes": dict(st.session_state.observacoes),
        "timestamp": datetime.now().isoformat(),
    }

    # Salvar no session_state
    st.session_state.dados_visita = dados_visita

    st.success(f"Relatório finalizado! {emoji} **{resultado['percentual']}% — {label_cls}**")
    st.balloons()

# ──────────────────────────────────────────────────
# RESULTADO (persiste após rerun graças ao session_state)
# ──────────────────────────────────────────────────

if st.session_state.enviado and "dados_visita" in st.session_state:
    dados_visita = st.session_state.dados_visita
    resultado = dados_visita["resultado"]

    # ── DASHBOARD COMPLETO ──
    st.markdown("---")
    st.subheader("📊 Resultado da Visita")
    renderizar_dashboard(resultado, dados_visita)

    # ── PLANO DE AÇÃO ──
    st.markdown("---")
    st.subheader("📝 Plano de Ação")
    st.caption("Descreva as ações corretivas, prazos e responsáveis. Se deixar em branco, esta seção não aparecerá no PDF.")

    plano_acao = st.text_area(
        "Plano de Ação",
        placeholder="Ex: Realizar treinamento de BPF até 15/06. Responsável: Andre.\nSolicitar dedetização emergencial até 20/06. Responsável: Caio.",
        height=150,
        key="plano_acao",
        label_visibility="collapsed",
    )

    # ── GERAR PDF ──
    st.markdown("---")
    st.subheader("📄 Relatório PDF")

    if st.button("🔄  Gerar PDF", key="btn_gerar_pdf"):
        dados_visita_pdf = dict(dados_visita)
        dados_visita_pdf["plano_acao"] = plano_acao.strip() if plano_acao else ""
        st.session_state.pdf_bytes = bytes(gerar_pdf(dados_visita_pdf))
        st.session_state.pdf_nome = (
            f"relatorio_{dados_visita['unidade'].replace(' ', '_')}"
            f"_{dados_visita['data_visita'].replace('/', '')}.pdf"
        )
        st.rerun()

    # Mostrar botão de download se o PDF já foi gerado
    if "pdf_bytes" in st.session_state:
        st.success("✅ PDF gerado com sucesso! Clique abaixo para baixar.")
        st.download_button(
            label="📥  Baixar Relatório em PDF",
            data=st.session_state.pdf_bytes,
            file_name=st.session_state.get("pdf_nome", "relatorio.pdf"),
            mime="application/pdf",
        )

    # ── ENVIAR POR WHATSAPP ──
    st.markdown("---")
    st.subheader("💬 Enviar por WhatsApp")
    st.caption("Abre o WhatsApp com o resumo da visita. Anexe o PDF manualmente após abrir.")

    dados_visita_wa = dict(dados_visita)
    dados_visita_wa["plano_acao"] = plano_acao.strip() if plano_acao else ""

    url_whatsapp, msg_preview = gerar_link_whatsapp(dados_visita_wa)

    with st.expander("👁️ Pré-visualizar mensagem", expanded=False):
        st.text(msg_preview)

    st.link_button(
        label="💬  Enviar Relatório no WhatsApp",
        url=url_whatsapp,
    )


# ──────────────────────────────────────────────────
# BOTÃO LIMPAR
# ──────────────────────────────────────────────────

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

col_limpar1, col_limpar2, col_limpar3 = st.columns([2, 1, 2])

with col_limpar2:
    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        st.session_state.respostas = {}
        st.session_state.observacoes = {}
        st.session_state.enviado = False
        for key in ["dados_visita", "pdf_bytes", "pdf_nome"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# ──────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div class="brand-footer">
    <div class="gold-line"></div>
    CAIO COUTO NUTRICIONISTA<br>
    Consultoria de Alimentos &middot; RDC 216/2004 &mdash; ANVISA
</div>
""", unsafe_allow_html=True)
