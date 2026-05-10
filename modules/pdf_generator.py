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
    # SCORECARD — NOTA GERAL
    # ══════════════════════════════════════════════

    pdf._section_title("Resultado Geral")

    # Caixa colorida com a nota
    x_start = 60
    box_w = 90
    box_h = 25
    y_start = pdf.get_y()

    pdf.set_fill_color(*cor_rgb)
    pdf.set_draw_color(*cor_rgb)
    pdf.rect(x_start, y_start, box_w, box_h, style="DF")

    # Percentual grande
    pdf.set_xy(x_start, y_start + 2)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(*BRANCO)
    pdf.cell(box_w, 12, f"{resultado['percentual']}%", align="C", ln=True)

    # Label
    pdf.set_x(x_start)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(box_w, 8, _safe(label_cls), align="C", ln=True)

    pdf.set_y(y_start + box_h + 3)

    # Pontuação
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*CINZA)
    pdf.cell(0, 5,
             f"{resultado['total_obtido']} de {resultado['total_maximo']} pontos  ·  "
             f"{len(resultado['nao_conformidades'])} não conformidade(s)",
             align="C", ln=True)
    pdf.ln(4)

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
    # GRÁFICO DE EVOLUÇÃO (últimas 10 visitas)
    # ══════════════════════════════════════════════

    try:
        from modules.dashboard import carregar_historico
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
        import tempfile

        historico = carregar_historico()
        unidade_atual = dados_visita.get("unidade", "")

        # Filtrar pela unidade atual e pegar as últimas 10
        hist_unidade = [h for h in historico if h.get("unidade") == unidade_atual]

        if len(hist_unidade) >= 2:
            import pandas as pd_hist
            df_hist = pd_hist.DataFrame(hist_unidade)
            df_hist["data_dt"] = pd_hist.to_datetime(df_hist["data_visita"], format="%d/%m/%Y", errors="coerce")
            df_hist = df_hist.sort_values("data_dt").tail(10)

            fig_mpl, ax = plt.subplots(figsize=(8, 3.2), dpi=150)

            # Linha principal
            ax.plot(
                df_hist["data_visita"].values,
                df_hist["percentual_geral"].values,
                color="#1B4F72", linewidth=2, marker="o", markersize=6,
                zorder=5,
            )

            # Labels nos pontos
            for _, row in df_hist.iterrows():
                ax.annotate(
                    f"{row['percentual_geral']:.0f}%",
                    (row["data_visita"], row["percentual_geral"]),
                    textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=7, color="#1B4F72", fontweight="bold",
                )

            # Faixas de referência
            ax.axhline(y=90, color="#1a5e1a", linestyle="--", linewidth=0.8, alpha=0.7)
            ax.axhline(y=80, color="#27ae60", linestyle="--", linewidth=0.8, alpha=0.7)
            ax.axhline(y=70, color="#f39c12", linestyle="--", linewidth=0.8, alpha=0.7)

            # Labels das faixas
            ax.text(len(df_hist) - 0.5, 91, "Excelente", fontsize=6, color="#1a5e1a", va="bottom")
            ax.text(len(df_hist) - 0.5, 81, "Bom", fontsize=6, color="#27ae60", va="bottom")
            ax.text(len(df_hist) - 0.5, 71, "Atencao", fontsize=6, color="#f39c12", va="bottom")

            ax.set_ylim(0, 105)
            ax.set_ylabel("Conformidade (%)", fontsize=8)
            ax.set_xlabel("Data da Visita", fontsize=8)
            ax.tick_params(axis="both", labelsize=7)
            plt.xticks(rotation=45, ha="right")
            ax.grid(axis="y", alpha=0.3)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            plt.tight_layout()

            # Salvar como PNG temporário
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                fig_mpl.savefig(tmp.name, format="png", bbox_inches="tight")
                tmp_path = tmp.name
            plt.close(fig_mpl)

            # Nova página se necessário
            if pdf.get_y() > 160:
                pdf.add_page()

            pdf._section_title(_safe(f"Evolucao - {unidade_atual} (ultimas {len(df_hist)} visitas)"))

            # Centralizar imagem
            img_w = 170
            img_x = (210 - img_w) / 2
            pdf.image(tmp_path, x=img_x, y=pdf.get_y(), w=img_w)
            pdf.ln(75)

            os.remove(tmp_path)

    except Exception:
        pass  # Se falhar, pula silenciosamente

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
                pdf.cell(12, 4, "", ln=False)
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

    return pdf.output()
