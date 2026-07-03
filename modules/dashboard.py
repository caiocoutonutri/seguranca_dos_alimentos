# modules/dashboard.py
# Dashboard de Conformidade — Consultoria Mariner
# Gráficos Plotly + Pandas para análise pós-visita
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.formulario import classificar_nota, SECOES
import os
from datetime import datetime
import requests
import base64
from io import StringIO

# ──────────────────────────────────────────────────
# CORES DO TEMA
# ──────────────────────────────────────────────────

CORES = {
    "excelente": "#1a5e1a",
    "bom": "#27ae60",
    "atencao": "#f39c12",
    "critico": "#e74c3c",
    "fundo": "#f8f9fa",
    "texto": "#1C1C1C",
    "azul": "#1B4F72",
    "azul_claro": "#3498db",
    "cinza": "#95a5a6",
}


def cor_por_percentual(pct):
    """Retorna cor hex baseada no percentual."""
    if pct >= 90:
        return CORES["excelente"]
    elif pct >= 80:
        return CORES["bom"]
    elif pct >= 70:
        return CORES["atencao"]
    else:
        return CORES["critico"]

# ──────────────────────────────────────────────────
# GRÁFICO DE BARRAS HORIZONTAIS
# ──────────────────────────────────────────────────

def grafico_barras(resultado):
    """
    Barras horizontais com % de conformidade por seção.
    Ordenadas da menor para maior conformidade (piores no topo).
    """
    secoes_com_dados = [s for s in resultado["secoes"] if s["maximo"] > 0]

    df = pd.DataFrame(secoes_com_dados)
    df["label"] = df.apply(lambda r: f"{r['numero']}. {r['titulo']}", axis=1)
    df["cor"] = df["percentual"].apply(cor_por_percentual)
    df = df.sort_values("percentual", ascending=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["percentual"],
        y=df["label"],
        orientation="h",
        marker=dict(
            color=df["cor"],
            line=dict(color="white", width=1),
        ),
        text=df["percentual"].apply(lambda x: f"{x:.0f}%"),
        textposition="auto",
        textfont=dict(color="white", size=12, family="Arial Black"),
        hovertemplate="%{y}<br>%{x:.1f}%<extra></extra>",
    ))

    # Linhas de referência verticais
    for faixa, cor in [(70, CORES["atencao"]), (80, CORES["bom"]), (90, CORES["excelente"])]:
        fig.add_vline(
            x=faixa, line_dash="dot", line_color=cor, line_width=1,
            annotation_text=f"{faixa}%", annotation_position="top",
            annotation_font=dict(size=9, color=cor),
        )

    fig.update_layout(
        xaxis=dict(
            range=[0, 105],
            title="Conformidade (%)",
            ticksuffix="%",
        ),
        yaxis=dict(
            title="",
            automargin=True,
        ),
        margin=dict(l=10, r=20, t=20, b=50),
        height=max(350, len(df) * 38),
        showlegend=False,
    )

    return fig


# ──────────────────────────────────────────────────
# TABELA RESUMO
# ──────────────────────────────────────────────────

def tabela_resumo(resultado):
    """
    Retorna DataFrame formatado com resumo por seção.
    """
    linhas = []
    for sec in resultado["secoes"]:
        emoji, label, _ = classificar_nota(sec["percentual"]) if sec["maximo"] > 0 else ("⚪", "N/A", "#ccc")
        linhas.append({
            "Seção": f"{sec['numero']}. {sec['titulo']}",
            "Obtido": sec["obtido"],
            "Máximo": sec["maximo"],
            "Conformidade": f"{sec['percentual']}%" if sec["maximo"] > 0 else "N/A",
            "Status": f"{emoji} {label}",
        })

    # Linha total
    emoji_t, label_t, _ = resultado["classificacao"]
    linhas.append({
        "Seção": "TOTAL",
        "Obtido": resultado["total_obtido"],
        "Máximo": resultado["total_maximo"],
        "Conformidade": f"{resultado['percentual']}%",
        "Status": f"{emoji_t} {label_t}",
    })

    return pd.DataFrame(linhas)


# ──────────────────────────────────────────────────
# HISTÓRICO — salvar e carregar visitas (CSV)
# ──────────────────────────────────────────────────

HISTORICO_PATH = os.path.join("data", "historico_visitas.csv")

# Colunas fixas do CSV
_COLUNAS_BASE = [
    "unidade", "data_visita", "nutricionista", "responsavel",
    "timestamp", "percentual_geral", "total_obtido", "total_maximo",
    "classificacao", "nao_conformidades_qtd",
]

# Colunas de % por seção: secao_1_pct, secao_2_pct, ..., secao_17_pct
_COLUNAS_SECOES = [f"secao_{s['numero']}_pct" for s in SECOES]

COLUNAS_CSV = _COLUNAS_BASE + _COLUNAS_SECOES

def _obter_config_github():
    token = st.secrets.get("TOKEN_GITHUB", "")
    usuario = st.secrets.get("GITHUB_USER", "caiocoutonutri")
    repositorio = st.secrets.get("GITHUB_REPO", "seguranca_dos_alimentos")
    branch = st.secrets.get("GITHUB_BRANCH", "main")
    return token, usuario, repositorio, branch

def carregar_historico_do_github():
    token, usuario, repositorio, branch = _obter_config_github()

    if not token:
        return None, None

    caminho = "data/historico_visitas.csv"
    url = f"https://api.github.com/repos/{usuario}/{repositorio}/contents/{caminho}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    response_get = requests.get(url, headers=headers, params={"ref": branch})

    if response_get.status_code == 404:
        return pd.DataFrame(columns=COLUNAS_CSV), None

    if response_get.status_code != 200:
        st.warning(f"Não foi possível carregar histórico do GitHub: {response_get.status_code} - {response_get.text}")
        return None, None

    dados = response_get.json()
    sha = dados.get("sha")
    conteudo_b64 = dados.get("content", "")
    conteudo_csv = base64.b64decode(conteudo_b64).decode("utf-8-sig")

    if not conteudo_csv.strip():
        return pd.DataFrame(columns=COLUNAS_CSV), sha

    df = pd.read_csv(StringIO(conteudo_csv), encoding="utf-8-sig")
    return df, sha


def atualizar_historico_no_github(df_historico, sha=None):
    token, usuario, repositorio, branch = _obter_config_github()

    if not token:
        st.warning("Histórico salvo localmente, mas TOKEN_GITHUB não está configurado no Streamlit secrets.")
        return False

    caminho = "data/historico_visitas.csv"
    url = f"https://api.github.com/repos/{usuario}/{repositorio}/contents/{caminho}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    buffer = StringIO()
    df_historico.to_csv(buffer, index=False, encoding="utf-8-sig")
    conteudo_csv = buffer.getvalue()
    conteudo_b64 = base64.b64encode(conteudo_csv.encode("utf-8-sig")).decode("utf-8")

    payload = {
        "message": "Atualiza historico_visitas.csv via Streamlit",
        "content": conteudo_b64,
        "branch": branch,
    }

    if sha:
        payload["sha"] = sha

    response_put = requests.put(url, headers=headers, json=payload)

    if response_put.status_code not in (200, 201):
        st.warning(f"Histórico salvo localmente, mas falhou ao atualizar GitHub: {response_put.status_code} - {response_put.text}")
        return False

    return True


def salvar_no_historico(dados_visita):
    """Salva a visita no CSV local e tenta persistir o histórico no GitHub."""
    os.makedirs("data", exist_ok=True)

    resultado = dados_visita["resultado"]

    linha = {
        "unidade": dados_visita["unidade"],
        "data_visita": dados_visita["data_visita"],
        "nutricionista": dados_visita["nutricionista"],
        "responsavel": dados_visita["responsavel"],
        "timestamp": dados_visita["timestamp"],
        "percentual_geral": resultado["percentual"],
        "total_obtido": resultado["total_obtido"],
        "total_maximo": resultado["total_maximo"],
        "classificacao": resultado["classificacao"][1],
        "nao_conformidades_qtd": len(resultado["nao_conformidades"]),
    }

    for sec in resultado["secoes"]:
        col = f"secao_{sec['numero']}_pct"
        linha[col] = sec["percentual"]

    df_novo = pd.DataFrame([linha])

    df_atual_github, sha = carregar_historico_do_github()

    if df_atual_github is not None:
        df_atual = df_atual_github
    else:
        if os.path.exists(HISTORICO_PATH) and os.path.getsize(HISTORICO_PATH) > 10:
            try:
                df_atual = pd.read_csv(HISTORICO_PATH, encoding="utf-8-sig")
            except Exception:
                df_atual = pd.DataFrame(columns=COLUNAS_CSV)
        else:
            df_atual = pd.DataFrame(columns=COLUNAS_CSV)
        sha = None

    df_historico = pd.concat([df_atual, df_novo], ignore_index=True)

    for col in COLUNAS_CSV:
        if col not in df_historico.columns:
            df_historico[col] = None

    df_historico = df_historico[COLUNAS_CSV]

    df_historico.to_csv(HISTORICO_PATH, index=False, encoding="utf-8-sig")

    github_ok = atualizar_historico_no_github(df_historico, sha=sha)

    return {
        "linha": linha,
        "github_ok": github_ok,
    }

def carregar_historico():
    """
    Carrega o histórico de visitas do CSV.
    Retorna lista de dicts (compatível com o resto do código).
    Tolera linhas com número diferente de colunas (ex: seções foram alteradas).
    """
    if not os.path.exists(HISTORICO_PATH):
        return []
    try:
        # Primeiro tenta leitura normal
        df = pd.read_csv(HISTORICO_PATH, encoding="utf-8-sig")
        if df.empty or "unidade" not in df.columns:
            return []
        return df.to_dict("records")
    except Exception:
        pass

    # Se falhou (colunas inconsistentes), ler linha por linha
    try:
        linhas = []
        with open(HISTORICO_PATH, "r", encoding="utf-8-sig") as f:
            header = f.readline().strip().split(",")
            for raw_line in f:
                valores = raw_line.strip().split(",")
                # Usar apenas as colunas do header (truncar ou preencher)
                row = {}
                for i, col in enumerate(header):
                    row[col] = valores[i] if i < len(valores) else ""
                linhas.append(row)

        if not linhas:
            return []

        df = pd.DataFrame(linhas)
        if "unidade" not in df.columns:
            return []

        # Converter colunas numéricas
        for col in df.columns:
            if col.startswith("secao_") or col in ("percentual_geral", "total_obtido", "total_maximo", "nao_conformidades_qtd"):
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df.to_dict("records")
    except Exception:
        return []


def carregar_historico_df():
    """Carrega o histórico como DataFrame (para uso direto em gráficos)."""
    historico = carregar_historico()
    if not historico:
        return pd.DataFrame(columns=_COLUNAS_BASE)
    return pd.DataFrame(historico)


# ──────────────────────────────────────────────────
# GRÁFICO DE EVOLUÇÃO HISTÓRICA
# ──────────────────────────────────────────────────
def grafico_evolucao(unidade_filtro=None):
    historico = carregar_historico()

    if not historico:
        return None

    df = pd.DataFrame(historico)

    if unidade_filtro and unidade_filtro != "Todas":
        df = df[df["unidade"] == unidade_filtro]

    if df.empty:
        return None

    df["data_dt"] = pd.to_datetime(df["data_visita"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["data_dt"])

    df["unidade_label"] = df["unidade"].str.replace("Mariner — ", "", regex=False)

    # Limitar sempre às últimas 10 visitas por unidade
    df = (
        df.sort_values(["unidade_label", "data_dt"])
        .groupby("unidade_label", group_keys=False)
        .tail(10)
        .reset_index(drop=True)
    )

    cores_unidades = [
        CORES["azul"],
        CORES["bom"],
        CORES["atencao"],
        CORES["critico"],
        CORES["azul_claro"],
    ]

    unidades = df["unidade_label"].dropna().unique().tolist()

    fig = make_subplots(
        rows=len(unidades),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=unidades,
    )

    for i, unidade in enumerate(unidades):
        df_u = df[df["unidade_label"] == unidade]
        cor = cores_unidades[i % len(cores_unidades)]
        row = i + 1

        fig.add_trace(
            go.Scatter(
                x=df_u["data_dt"],
                y=df_u["percentual_geral"], 
                mode="lines+markers+text",
                name=unidade,
                legendgroup=unidade,
                line=dict(color=cor, width=3),
                marker=dict(size=9, color=cor),
                text=df_u["percentual_geral"].apply(lambda x: f"{x:.0f}%"),
                textposition="top center",
                textfont=dict(size=10, color=cor),
                hovertemplate=(
                    f"<b>{unidade}</b><br>"
                    "Data: %{x|%d/%m/%Y}<br>"
                    "Conformidade: %{y:.1f}%<br>"
                    "<extra></extra>"
                ),
            ),
            row=row,
            col=1,
        )

        fig.add_hline(
            y=90,
            line_dash="dot",
            line_color=CORES["excelente"],
            opacity=0.5,
            row=row,
            col=1,
        )

        fig.add_hline(
            y=80,
            line_dash="dot",
            line_color=CORES["bom"],
            opacity=0.4,
            row=row,
            col=1,
        )
        y_min = max(0, df_u["percentual_geral"].min() - 5)
        y_max = min(105, df_u["percentual_geral"].max() + 5)

        if y_max - y_min < 10:
            y_min = max(0, y_min - 5)
            y_max = min(105, y_max + 5)

        fig.update_yaxes(
            range=[y_min, y_max],
            ticksuffix="%",
            title_text="%",
            row=row,
            col=1,
        )

    # Datas só no gráfico de baixo
    for row in range(1, len(unidades)):
        fig.update_xaxes(
            showticklabels=False,
            title_text="",
            row=row,
            col=1,
        )

    fig.update_xaxes(
        title_text="Data da Visita",
        type="date",
        tickformat="%d/%m/%Y",
        tickangle=-45,
        row=len(unidades),
        col=1,
    )

    fig.update_layout(
        title="Evolução de Conformidade por Unidade",
        height=max(450, len(unidades) * 180),
        margin=dict(l=60, r=40, t=80, b=80),
        legend=dict(
            title="Unidade",
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
        ),
        showlegend=True,
    )

    return fig


# ──────────────────────────────────────────────────
# COMPARATIVO ENTRE UNIDADES
# ──────────────────────────────────────────────────

def grafico_comparativo_unidades():
    """
    Barras agrupadas mostrando a ÚLTIMA visita de cada unidade,
    para comparação direta entre os restaurantes.
    """
    historico = carregar_historico()

    if not historico:
        return None

    df = pd.DataFrame(historico)
    df["data_dt"] = pd.to_datetime(df["data_visita"], format="%d/%m/%Y", errors="coerce")

    # Pegar a última visita de cada unidade
    ultimas = df.sort_values("data_dt").groupby("unidade").last().reset_index()

    if ultimas.empty:
        return None

    ultimas["label"] = ultimas["unidade"].str.replace("Mariner — ", "")
    ultimas["cor"] = ultimas["percentual_geral"].apply(cor_por_percentual)
    ultimas = ultimas.sort_values("percentual_geral", ascending=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=ultimas["percentual_geral"],
        y=ultimas["label"],
        orientation="h",
        marker=dict(
            color=ultimas["cor"],
            line=dict(color="white", width=1),
        ),
        text=ultimas.apply(
            lambda r: f"{r['percentual_geral']:.0f}% ({r['data_visita']})", axis=1
        ),
        textposition="auto",
        textfont=dict(color="white", size=12, family="Arial Black"),
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"
            "Data: %{x|%d/%m/%Y}<br>"
            "Conformidade: %{y:.1f}%<br>"
            "<extra></extra>"
        ),
    ))

    for faixa, cor in [(70, CORES["atencao"]), (80, CORES["bom"]), (90, CORES["excelente"])]:
        fig.add_vline(x=faixa, line_dash="dot", line_color=cor, line_width=1)

    fig.update_layout(
        xaxis=dict(range=[0, 105], title="Conformidade (%)", ticksuffix="%"),
        yaxis=dict(title="", automargin=True),
        margin=dict(l=10, r=20, t=20, b=50),
        height=max(250, len(ultimas) * 55),
        showlegend=False,
    )

    return fig


# ──────────────────────────────────────────────────
# FUNÇÃO PRINCIPAL — renderizar dashboard no Streamlit
# ──────────────────────────────────────────────────

def renderizar_dashboard(resultado, dados_visita):
    """
    Renderiza o dashboard completo no Streamlit.
    Chamado após o envio do formulário.
    """

    emoji, label_cls, cor = resultado["classificacao"]

    # ── SCORECARD PREMIUM ──
    st.markdown(f"""
    <div class="scorecard-premium" style="text-align:center; padding:2.5rem 2rem; margin:1rem 0;
                background: linear-gradient(135deg, #1C1C1C 0%, #2D2D2D 100%);
                border-radius: 16px; position:relative; overflow:hidden;">
        <div style="position:absolute; top:0; left:0; right:0; height:3px;
                    background: linear-gradient(90deg, transparent, #C5A55A, transparent);"></div>
        <p class="gold-text" style="font-family:'Inter',sans-serif; font-size:0.75rem;
                  letter-spacing:3px; text-transform:uppercase; margin:0 0 0.8rem 0;">
            Conformidade Total
        </p>
        <h2 style="font-family:'Playfair Display',Georgia,serif;
                   font-size:3.5rem; font-weight:700; margin:0; line-height:1;">
            {resultado['percentual']}%
        </h2>
        <p style="font-family:'Inter',sans-serif; color:{cor}; font-weight:900;
                  font-size:1rem; margin:0.5rem 0 0 0; letter-spacing:1px;">
            {emoji} {label_cls.upper()}
        </p>
        <div style="width:40px; height:2px; background:#C5A55A; margin:0.8rem auto;"></div>
        <p class="grey-text" style="font-family:'Inter',sans-serif; font-size:0.8rem; margin:0;">
            {resultado['total_obtido']} de {resultado['total_maximo']} pontos
        </p>
        <div style="position:absolute; bottom:0; left:0; right:0; height:3px;
                    background: linear-gradient(90deg, transparent, #C5A55A, transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── GRÁFICOS EM TABS ──
    tab_barras, tab_tabela, tab_historico = st.tabs([
       "📊 Barras", "📋 Tabela", "📈 Histórico"
    ])

    with tab_barras:
        st.plotly_chart(grafico_barras(resultado), use_container_width=True)

    with tab_tabela:
        df_resumo = tabela_resumo(resultado)
        st.dataframe(
            df_resumo,
            use_container_width=True,
            hide_index=True,
            height=min(700, (len(df_resumo) + 1) * 38),
        )

    with tab_historico:
        try:
            historico = carregar_historico()

            if len(historico) <= 1:
                st.info(
                    "📌 Histórico disponível a partir da segunda visita. "
                    "Os dados desta visita já foram salvos."
                )
            else:
                # Filtro de unidade
                unidades_historico = sorted(set(
                    h.get("unidade", "") for h in historico if h.get("unidade")
                ))
                opcoes = ["Todas"] + unidades_historico
                filtro = st.selectbox("Filtrar por unidade:", opcoes, key="filtro_historico")

                # Evolução
                st.markdown("#### Evolução ao Longo do Tempo")
                fig_evo = grafico_evolucao(filtro)
                if fig_evo:
                    st.plotly_chart(fig_evo, use_container_width=True)

                # Comparativo entre unidades
                if len(unidades_historico) > 1:
                    st.markdown("#### Comparativo entre Unidades (Última Visita)")
                    fig_comp = grafico_comparativo_unidades()
                    if fig_comp:
                        st.plotly_chart(fig_comp, use_container_width=True)
        except Exception as e:
            st.warning(
                f"⚠️ Não foi possível carregar o histórico. "
                f"Se você alterou o número de seções, apague o arquivo "
                f"`data/historico_visitas.csv` e recomece.\n\nErro: {e}"
            )

    # ── NÃO CONFORMIDADES ──
    if resultado["nao_conformidades"]:
        st.markdown("---")
        with st.expander(
            f"⚠️ {len(resultado['nao_conformidades'])} Não Conformidades",
            expanded=True,
        ):
            for nc in resultado["nao_conformidades"]:
                obs_nc = dados_visita["observacoes"].get(nc["id"], "")
                obs_txt = f"  ·  _\"{obs_nc}\"_" if obs_nc else ""
                st.markdown(
                    f"🔴 **{nc['id']}** — {nc['texto']} "
                    f"(`-{nc['pontos_perdidos']} pts`){obs_txt}"
                )
    else:
        st.success("🎉 Nenhuma não conformidade encontrada!")
