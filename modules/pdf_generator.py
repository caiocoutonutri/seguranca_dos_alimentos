# modules/pdf_generator.py
# Gerador de PDF — Relatório de Visita Técnica
# Identidade visual: Caio Couto Nutricionista
# Cores: preto (#1C1C1C), dourado (#C5A55A), cinza (#666666)

import os
import io
import tempfile
from fpdf import FPDF
from modules.formulario import SECOES, classificar_nota


def _safe(text):
    """Sanitiza texto para fontes core do FPDF (latin-1)."""
    replacements = {
        "\u2014": "-",    # em-dash → hyphen
        "\u2013": "-",    # en-dash → hyphen
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u2022": "-",    # bullet
        "\u00b0": "o",    # degree (°C)
        "\u2265": ">=",   # ≥
        "\u2264": "<=",   # ≤
        "\u2212": "-",    # minus sign
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Fallback: replace any remaining non-latin1 chars
    try:
        text.encode("latin-1")
    except UnicodeEncodeError:
        text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text


# ──────────────────────────────────────────────────
# CORES DA MARCA
# ──────────────────────────────────────────────────

PRETO = (28, 28, 28)        # #1C1C1C
DOURADO = (197, 165, 90)    # #C5A55A
CINZA = (102, 102, 102)     # #666666
CINZA_CLARO = (240, 240, 240)  # #F0F0F0
BRANCO = (255, 255, 255)
VERDE_ESCURO = (26, 94, 26)    # #1a5e1a
VERDE = (39, 174, 96)          # #27ae60
AMARELO = (243, 156, 18)       # #f39c12
VERMELHO = (231, 76, 60)       # #e74c3c

LOGO_PATH = os.path.join("assets", "Logo-CC.PNG")


def cor_semaforo(percentual):
    """Retorna tupla RGB baseada no percentual."""
    if percentual >= 90:
        return VERDE_ESCURO
    elif percentual >= 80:
        return VERDE
    elif percentual >= 70:
        return AMARELO
    else:
        return VERMELHO


# ──────────────────────────────────────────────────
# CLASSE PDF CUSTOMIZADA
# ──────────────────────────────────────────────────

class RelatorioPDF(FPDF):
    """PDF customizado com header/footer da marca Caio Couto."""

    def __init__(self, dados_visita):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.dados = dados_visita
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        # Bloco logo + texto centralizado na página (A4 = 210mm)
        # Logo 28mm + gap 5mm + texto ~100mm = ~133mm total
        # Margem esquerda = (210 - 133) / 2 ≈ 38mm
        logo_top = 10
        logo_w = 28
        logo_x = 60
        text_x = logo_x + logo_w + 5  # 71

        if os.path.exists(LOGO_PATH):
            self.image(LOGO_PATH, x=logo_x, y=logo_top, w=logo_w)

        # Título — centralizado verticalmente com a logo
        self.set_xy(text_x, 19)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(*PRETO)
        self.cell(0, 6, _safe("Relatorio de Visita Tecnica"), ln=True)

        self.set_xy(text_x, 26)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*CINZA)
        self.cell(0, 5, _safe("RDC 216 - Seguranca dos Alimentos"), ln=True)

        # Linha dourada
        linha_y = logo_top + logo_w + 4
        self.set_draw_color(*DOURADO)
        self.set_line_width(0.5)
        self.line(10, linha_y, 200, linha_y)

        self.set_y(linha_y + 5)

    def footer(self):
        self.set_y(-20)

        # Linha dourada
        self.set_draw_color(*DOURADO)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())

        self.ln(3)
        self.set_font("Helvetica", "", 7)
        self.set_text_color(*CINZA)
        self.cell(0, 4, "Caio Couto Nutricionista · Consultoria de Alimentos", align="C", ln=True)
        self.cell(0, 4, _safe(f"Baseado na RDC no 216/2004 - ANVISA - Pagina {self.page_no()}/{{nb}}"), align="C")

    def _section_title(self, text):
        """Título de seção com fundo cinza claro."""
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*PRETO)
        self.set_fill_color(*CINZA_CLARO)
        self.cell(0, 8, _safe(f"  {text}"), ln=True, fill=True)
        self.ln(2)

    def _label_value(self, label, value, bold_value=False):
        """Par label: valor em uma linha."""
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*CINZA)
        self.cell(40, 5, _safe(label), ln=False)
        self.set_text_color(*PRETO)
        self.set_font("Helvetica", "B" if bold_value else "", 9)
        self.cell(0, 5, _safe(str(value)), ln=True)


# ──────────────────────────────────────────────────
# FUNÇÃO PRINCIPAL
# ──────────────────────────────────────────────────

def gerar_pdf(dados_visita):
    """
    Gera o PDF do relatório de visita técnica.

    Args:
        dados_visita: dict com unidade, data_visita, responsavel,
                      nutricionista, resultado, observacoes, etc.

    Returns:
        bytes: conteúdo do PDF em bytes (para st.download_button)
    """
    resultado = dados_visita["resultado"]
    emoji, label_cls, cor_hex = resultado["classificacao"]
    cor_rgb = cor_semaforo(resultado["percentual"])

    pdf = RelatorioPDF(dados_visita)
    pdf.alias_nb_pages()
    pdf.add_page()

    # ══════════════════════════════════════════════
    # INFORMAÇÕES DA VISITA
    # ══════════════════════════════════════════════

    pdf._section_title("Informações da Visita")

    pdf._label_value("Unidade:", dados_visita["unidade"], bold_value=True)
    pdf._label_value("Data da Visita:", dados_visita["data_visita"])
    pdf._label_value("Responsável Técnico:", dados_visita["responsavel"])
    pdf._label_value("Nutricionista:", dados_visita["nutricionista"])
    pdf.ln(4)

    # ══════════════════════════════════════════════
    # SCORECARD — DESIGN PREMIUM
    # ══════════════════════════════════════════════

    y_start = pdf.get_y() + 2
    box_x = 30
    box_w = 150
    box_h = 35

    # Fundo escuro
    pdf.set_fill_color(*PRETO)
    pdf.set_draw_color(*PRETO)
    pdf.rect(box_x, y_start, box_w, box_h, style="DF")

    # Linha dourada no topo
    pdf.set_draw_color(*DOURADO)
    pdf.set_line_width(0.8)
    pdf.line(box_x + 30, y_start, box_x + box_w - 30, y_start)

    # "CONFORMIDADE TOTAL" em dourado
    pdf.set_xy(box_x, y_start + 3)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*DOURADO)
    pdf.cell(box_w, 4, "CONFORMIDADE TOTAL", align="C", ln=True)

    # Percentual grande em dourado
    pdf.set_x(box_x)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*DOURADO)
    pdf.cell(box_w, 14, f"{resultado['percentual']}%", align="C", ln=True)

    # Label da classificação com cor do semáforo
    pdf.set_x(box_x)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(*cor_rgb)
    pdf.cell(box_w, 5, _safe(label_cls.upper()), align="C", ln=True)

    # Linha dourada embaixo
    pdf.set_draw_color(*DOURADO)
    pdf.line(box_x + 30, y_start + box_h, box_x + box_w - 30, y_start + box_h)

    pdf.set_y(y_start + box_h + 4)

    # Pontuação em cinza
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*CINZA)
    pdf.cell(0, 5,
             _safe(f"{resultado['total_obtido']} de {resultado['total_maximo']} pontos  -  "
             f"{len(resultado['nao_conformidades'])} nao conformidade(s)"),
             align="C", ln=True)
    pdf.ln(6)

    # ══════════════════════════════════════════════
    # TABELA DE PONTUAÇÃO POR SEÇÃO
    # ══════════════════════════════════════════════

    pdf._section_title("Pontuação por Seção")

    # Header da tabela
    col_widths = [80, 25, 25, 30, 30]
    headers = ["Seção", "Obtido", "Máximo", "Conform.", "Status"]

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*PRETO)
    pdf.set_text_color(*BRANCO)

    for i, (header, w) in enumerate(zip(headers, col_widths)):
        pdf.cell(w, 7, header, border=1, fill=True, align="C")
    pdf.ln()

    # Linhas da tabela
    pdf.set_font("Helvetica", "", 8)
    for idx, sec in enumerate(resultado["secoes"]):
        # Cor alternada
        if idx % 2 == 0:
            pdf.set_fill_color(250, 250, 250)
        else:
            pdf.set_fill_color(*BRANCO)

        cor_sec = cor_semaforo(sec["percentual"]) if sec["maximo"] > 0 else CINZA
        _, label_sec, _ = classificar_nota(sec["percentual"]) if sec["maximo"] > 0 else ("", "N/A", "")

        pdf.set_text_color(*PRETO)
        pdf.cell(col_widths[0], 6, _safe(f"{sec['numero']}. {sec['titulo']}"), border=1, fill=True)
        pdf.cell(col_widths[1], 6, str(sec["obtido"]), border=1, fill=True, align="C")
        pdf.cell(col_widths[2], 6, str(sec["maximo"]), border=1, fill=True, align="C")

        # % com cor
        pdf.set_text_color(*cor_sec)
        pct_text = f"{sec['percentual']}%" if sec["maximo"] > 0 else "N/A"
        pdf.cell(col_widths[3], 6, pct_text, border=1, fill=True, align="C")

        pdf.cell(col_widths[4], 6, _safe(label_sec), border=1, fill=True, align="C")
        pdf.set_text_color(*PRETO)
        pdf.ln()

    # Linha TOTAL
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(*CINZA_CLARO)
    pdf.cell(col_widths[0], 7, "TOTAL", border=1, fill=True)
    pdf.cell(col_widths[1], 7, str(resultado["total_obtido"]), border=1, fill=True, align="C")
    pdf.cell(col_widths[2], 7, str(resultado["total_maximo"]), border=1, fill=True, align="C")
    pdf.set_text_color(*cor_rgb)
    pdf.cell(col_widths[3], 7, f"{resultado['percentual']}%", border=1, fill=True, align="C")
    pdf.cell(col_widths[4], 7, _safe(label_cls), border=1, fill=True, align="C")
    pdf.set_text_color(*PRETO)
    pdf.ln(12)


    # ══════════════════════════════════════════════
    # EVOLUÇÃO HISTÓRICA POR UNIDADE (últimas 10 visitas)
    # ══════════════════════════════════════════════

    try:
        from modules.dashboard import carregar_historico
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import tempfile
        import pandas as pd_hist

        historico = carregar_historico()

        if historico:
            df_hist = pd_hist.DataFrame(historico)

            df_hist["data_dt"] = pd_hist.to_datetime(
                df_hist["data_visita"],
                format="%d/%m/%Y",
                errors="coerce",
            )

            df_hist["percentual_geral"] = pd_hist.to_numeric(
                df_hist["percentual_geral"],
                errors="coerce",
            )

            df_hist = df_hist.dropna(subset=["data_dt", "percentual_geral", "unidade"])

            df_hist["unidade_label"] = (
                df_hist["unidade"]
                .astype(str)
                .str.replace("Mariner — ", "", regex=False)
            )

            df_hist = (
                df_hist.sort_values(["unidade_label", "data_dt"])
                    .groupby("unidade_label", group_keys=False)
                    .tail(10)
                    .reset_index(drop=True)
            )

            unidades = df_hist["unidade_label"].dropna().unique().tolist()

            if len(unidades) >= 1:
                cores = ["#1B4F72", "#27ae60", "#f39c12", "#e74c3c", "#3498db"]

                fig_mpl, axes = plt.subplots(
                    nrows=len(unidades),
                    ncols=1,
                    figsize=(10, max(2.0, len(unidades) * 1.65)),
                    dpi=130,
                    sharex=True,
                )

                if len(unidades) == 1:
                    axes = [axes]


                # Eixo X global: todas as datas existentes no histórico limitado às últimas 10 por unidade
                datas_globais_dt = (
                    df_hist["data_dt"]
                    .drop_duplicates()
                    .sort_values()
                    .tolist()
                )

                datas_globais = [
                    data.strftime("%d/%m/%Y")
                    for data in datas_globais_dt
                ]

                mapa_x = {
                    data.strftime("%d/%m/%Y"): pos
                    for pos, data in enumerate(datas_globais_dt)
                }

                x_ticks = list(range(len(datas_globais)))

                for idx, unidade in enumerate(unidades):
                    ax = axes[idx]
                    df_u = df_hist[df_hist["unidade_label"] == unidade].copy()

                    datas = df_u["data_dt"].dt.strftime("%d/%m/%Y").tolist()
                    valores = df_u["percentual_geral"].tolist()
                    cor = cores[idx % len(cores)]
                    x_pos = [mapa_x[data] for data in datas]

                    ax.plot(
                        x_pos,
                        valores,
                        color=cor,
                        linewidth=2,
                        marker="o",
                        markersize=5,
                        zorder=5,
                    )

                    for x, v in zip(x_pos, valores):
                        ax.annotate(
                            f"{v:.0f}%",
                            (x, v),
                            textcoords="offset points",
                            xytext=(0, 7),
                            ha="center",
                            fontsize=7,
                            color=cor,
                            fontweight="bold",
                        )

                    # Faixas de referência
                    ax.axhline(y=90, color="#1a5e1a", linestyle="--", linewidth=0.7, alpha=0.6)
                    ax.axhline(y=80, color="#27ae60", linestyle="--", linewidth=0.7, alpha=0.5)
                    ax.axhline(y=70, color="#f39c12", linestyle="--", linewidth=0.7, alpha=0.5)

                    y_min = max(0, min(valores) - 5)
                    y_max = min(105, max(valores) + 5)

                    if y_max - y_min < 10:
                        y_min = max(0, y_min - 5)
                        y_max = min(105, y_max + 5)

                    ax.set_ylim(y_min, y_max)
                    ax.set_title(unidade, fontsize=10, fontweight="bold", color="#666666", pad=8)
                    ax.set_ylabel("%", fontsize=8)
                    ax.tick_params(axis="y", labelsize=7)
                    ax.grid(axis="y", alpha=0.25)
                    ax.spines["top"].set_visible(False)
                    ax.spines["right"].set_visible(False)

                    # Mesmo eixo X para todos, mas datas visíveis só no último gráfico
                    ax.set_xlim(-0.5, len(datas_globais) - 0.5)

                    if idx < len(unidades) - 1:
                        ax.tick_params(axis="x", labelbottom=False)
                        ax.set_xlabel("")
                    else:
                        ax.set_xticks(x_ticks)
                        ax.set_xticklabels(datas_globais, rotation=45, ha="right", fontsize=7)
                        ax.set_xlabel("Data da Visita", fontsize=8)

                fig_mpl.subplots_adjust(
                    left=0.08,
                    right=0.96,
                    top=0.95,
                    bottom=0.14,
                    hspace=0.55,
                )

                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                    fig_mpl.savefig(tmp.name, format="png", bbox_inches="tight")
                    tmp_path = tmp.name

                plt.close(fig_mpl)

                if pdf.get_y() > 120:
                    pdf.add_page()

                pdf._section_title("Evolucao Historica por Unidade - ultimas 10 visitas")

                img_w = 175
                img_x = (210 - img_w) / 2

                y_inicio = pdf.get_y()

                pdf.image(tmp_path, x=img_x, y=y_inicio, w=img_w)

                # altura REAL ocupada pela imagem
                altura_img = img_w * (fig_mpl.get_figheight() / fig_mpl.get_figwidth())

                pdf.set_y(y_inicio + altura_img + 4)


                os.remove(tmp_path)

                # ══════════════════════════════════════════════
                # MÉDIA HISTÓRICA POR UNIDADE
                # ══════════════════════════════════════════════

                df_media = (
                    df_hist.groupby("unidade_label", as_index=False)
                    .agg(
                        media_percentual=("percentual_geral", "mean"),
                        qtd_visitas=("percentual_geral", "count"),
                    )
                )

                df_media["media_percentual"] = df_media["media_percentual"].round(1)

                # Manter a mesma lógica de cores do gráfico de linhas
                mapa_cores = {
                    unidade: cores[idx % len(cores)]
                    for idx, unidade in enumerate(unidades)
                }

                df_media["cor"] = df_media["unidade_label"].map(mapa_cores)

                # Ordena para leitura em ranking no gráfico horizontal
                df_media = df_media.sort_values("media_percentual", ascending=True)

                fig_bar, ax_bar = plt.subplots(figsize=(10, 3.2), dpi=130)

                ax_bar.barh(
                    df_media["unidade_label"],
                    df_media["media_percentual"],
                    color=df_media["cor"],
                )

                for i, row in df_media.iterrows():
                    ax_bar.text(
                        row["media_percentual"] + 1,
                        row["unidade_label"],
                        f"{row['media_percentual']:.1f}% ({int(row['qtd_visitas'])} visitas)",
                        va="center",
                        fontsize=8,
                        fontweight="bold",
                        color="#333333",
                    )

                # Linhas de referência
                ax_bar.axvline(x=90, color="#1a5e1a", linestyle="--", linewidth=0.8, alpha=0.7)
                ax_bar.axvline(x=80, color="#27ae60", linestyle="--", linewidth=0.8, alpha=0.6)
                ax_bar.axvline(x=70, color="#f39c12", linestyle="--", linewidth=0.8, alpha=0.6)

                ax_bar.set_xlim(0, 105)
                ax_bar.set_xlabel("Media de Conformidade (%)", fontsize=8)
                ax_bar.tick_params(axis="x", labelsize=7)
                ax_bar.tick_params(axis="y", labelsize=8)
                ax_bar.grid(axis="x", alpha=0.25)
                ax_bar.spines["top"].set_visible(False)
                ax_bar.spines["right"].set_visible(False)

                fig_bar.subplots_adjust(left=0.18, right=0.92, top=0.92, bottom=0.22)

                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_bar:
                    fig_bar.savefig(tmp_bar.name, format="png", bbox_inches="tight")
                    tmp_bar_path = tmp_bar.name

                plt.close(fig_bar)

                pdf._section_title("Media Historica por Unidade")

                img_w_bar = 170
                img_x_bar = (210 - img_w_bar) / 2
                y_inicio = pdf.get_y()

                pdf.image(
                    tmp_bar_path,
                    x=img_x_bar,
                    y=y_inicio,
                    w=img_w_bar,
                )

                altura_bar = img_w_bar * (
                    fig_bar.get_figheight() / fig_bar.get_figwidth()
                )

                pdf.set_y(y_inicio + altura_bar + 4)

                os.remove(tmp_bar_path)


    except Exception as e:
        import traceback
        print("ERRO AO GERAR GRAFICO HISTORICO NO PDF:")
        print(e)
        print(traceback.format_exc())

    # ══════════════════════════════════════════════
    # NÃO CONFORMIDADES
    # ══════════════════════════════════════════════

    if resultado["nao_conformidades"]:
        # Verificar se precisa de nova página
        if pdf.get_y() > 230:
            pdf.add_page()

        pdf._section_title(f"Não Conformidades ({len(resultado['nao_conformidades'])})")

        for nc in resultado["nao_conformidades"]:
            # Verificar espaço
            if pdf.get_y() > 260:
                pdf.add_page()

            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(*VERMELHO)
            pdf.cell(12, 5, f"[{nc['id']}]", ln=False)

            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*PRETO)
            texto_nc = _safe(f"{nc['texto']}  (-{nc['pontos_perdidos']} pts)")
            pdf.multi_cell(0, 5, _safe(texto_nc))

            # Observação se houver
            obs = dados_visita.get("observacoes", {}).get(nc["id"], "")
            if obs:
                pdf.set_font("Helvetica", "I", 7)
                pdf.set_text_color(*CINZA)
                pdf.set_x(pdf.l_margin + 12)
                pdf.multi_cell(0, 4, _safe(f"Obs: {obs}"))

            pdf.ln(1)

    # ══════════════════════════════════════════════
    # OBSERVAÇÕES GERAIS POR SEÇÃO
    # ══════════════════════════════════════════════

    obs_gerais = []
    for secao in SECOES:
        obs_key = f"obs_secao_{secao['numero']}"
        obs = dados_visita.get("observacoes", {}).get(obs_key, "")
        if obs.strip():
            obs_gerais.append((secao["numero"], secao["titulo"], obs.strip()))

    if obs_gerais:
        if pdf.get_y() > 230:
            pdf.add_page()

        pdf._section_title("Observações Gerais por Seção")

        for num, titulo, obs in obs_gerais:
            if pdf.get_y() > 260:
                pdf.add_page()

            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(*PRETO)
            pdf.cell(0, 5, _safe(f"{num}. {titulo}"), ln=True)

            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(*CINZA)
            pdf.multi_cell(0, 4, _safe(obs))
            pdf.ln(2)

    # ══════════════════════════════════════════════
    # PLANO DE AÇÃO (só aparece se o nutricionista preencheu)
    # ══════════════════════════════════════════════

    plano_acao = dados_visita.get("plano_acao", "").strip()

    if plano_acao:
        if pdf.get_y() > 220:
            pdf.add_page()

        pdf._section_title("Plano de Acao")

        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*PRETO)
        pdf.multi_cell(0, 5, _safe(plano_acao))
        pdf.ln(4)

    # ══════════════════════════════════════════════
    # ASSINATURAS
    # ══════════════════════════════════════════════

    if pdf.get_y() > 240:
        pdf.add_page()

    pdf.ln(10)

    # Linha dourada antes das assinaturas
    pdf.set_draw_color(*DOURADO)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(8)

    # Duas colunas de assinatura
    y_assinatura = pdf.get_y()

    # Assinatura Nutricionista (esquerda)
    pdf.set_xy(20, y_assinatura)
    pdf.set_draw_color(*PRETO)
    pdf.set_line_width(0.2)

    # Imagem da assinatura do Caio (se existir)
    assinatura_path = os.path.join("assets", "assinatura_eng.png")
    if os.path.exists(assinatura_path):
        # Centralizar a assinatura acima da linha (largura 40mm, altura proporcional)
        sig_w = 40
        sig_x = 20 + (70 - sig_w) / 2  # centralizar nos 70mm da coluna
        pdf.image(assinatura_path, x=sig_x, y=y_assinatura - 2, w=sig_w)

    pdf.line(20, y_assinatura + 15, 90, y_assinatura + 15)

    pdf.set_xy(20, y_assinatura + 17)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*PRETO)
    pdf.cell(70, 4, _safe(dados_visita["nutricionista"]), align="C")

    pdf.set_xy(20, y_assinatura + 21)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*CINZA)
    pdf.cell(70, 4, "Nutricionista Avaliador", align="C")

    # Assinatura Responsável (direita)
    pdf.set_xy(120, y_assinatura)
    pdf.line(120, y_assinatura + 15, 190, y_assinatura + 15)

    pdf.set_xy(120, y_assinatura + 17)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*PRETO)
    pdf.cell(70, 4, _safe(dados_visita["responsavel"]), align="C")

    pdf.set_xy(120, y_assinatura + 21)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*CINZA)
    pdf.cell(70, 4, "Responsável da Unidade", align="C")

    # ══════════════════════════════════════════════
    # RETORNAR BYTES
    # ══════════════════════════════════════════════

    return bytes(pdf.output(dest="S"))
