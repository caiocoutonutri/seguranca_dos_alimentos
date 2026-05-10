# modules/whatsapp.py
# Gerador de link WhatsApp — Consultoria Mariner
# Envia mensagem pré-formatada com resumo da visita técnica

from urllib.parse import quote

# Número do Caio Couto (com código do país)
NUMERO_CAIO = "5521967100559"


def gerar_link_whatsapp(dados_visita):
    """
    Gera o link wa.me com mensagem pré-formatada.

    Args:
        dados_visita: dict com unidade, data_visita, responsavel,
                      nutricionista, resultado, etc.

    Returns:
        tuple: (url, mensagem_texto)
    """
    resultado = dados_visita["resultado"]
    emoji, label_cls, _ = resultado["classificacao"]

    # Montar resumo das seções
    resumo_secoes = ""
    for sec in resultado["secoes"]:
        if sec["maximo"] > 0:
            emoji_s, label_s, _ = _classificar_simples(sec["percentual"])
            resumo_secoes += f"  {emoji_s} {sec['numero']}. {sec['titulo']}: {sec['percentual']}%\n"

    # Montar lista de NCs (só as top 5 mais graves)
    ncs_texto = ""
    if resultado["nao_conformidades"]:
        ncs_ordenadas = sorted(
            resultado["nao_conformidades"],
            key=lambda x: x["pontos_perdidos"],
            reverse=True,
        )
        top_ncs = ncs_ordenadas[:5]
        ncs_texto = "\n*Principais não conformidades:*\n"
        for nc in top_ncs:
            ncs_texto += f"  ❌ [{nc['id']}] {nc['texto']} (-{nc['pontos_perdidos']} pts)\n"
        if len(ncs_ordenadas) > 5:
            ncs_texto += f"  ... e mais {len(ncs_ordenadas) - 5} item(ns)\n"

    # Plano de ação (se houver)
    plano_texto = ""
    plano = dados_visita.get("plano_acao", "").strip()
    if plano:
        plano_texto = f"\n*Plano de Ação:*\n{plano}\n"

    # Montar mensagem completa
    mensagem = (
        f"📋 *Relatório de Visita Técnica*\n"
        f"RDC 216 - Segurança dos Alimentos\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"\n"
        f"*Unidade:* {dados_visita['unidade']}\n"
        f"*Data:* {dados_visita['data_visita']}\n"
        f"*Responsável:* {dados_visita['responsavel']}\n"
        f"*Nutricionista:* {dados_visita['nutricionista']}\n"
        f"\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"{emoji} *Resultado: {resultado['percentual']}% — {label_cls}*\n"
        f"{resultado['total_obtido']} de {resultado['total_maximo']} pontos\n"
        f"\n"
        f"*Pontuação por seção:*\n"
        f"{resumo_secoes}"
        f"{ncs_texto}"
        f"{plano_texto}"
        f"\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📄 _Segue o PDF do relatório da visita técnica em anexo._\n"
        f"\n"
        f"_Caio Couto Nutricionista_\n"
        f"_Consultoria de Alimentos_"
    )

    url = f"https://wa.me/{NUMERO_CAIO}?text={quote(mensagem)}"

    return url, mensagem


def _classificar_simples(percentual):
    """Versão simples do classificar_nota para uso no WhatsApp."""
    if percentual >= 90:
        return "🟩", "Excelente", "#1a5e1a"
    elif percentual >= 80:
        return "🟢", "Bom", "#27ae60"
    elif percentual >= 70:
        return "🟡", "Atenção", "#f39c12"
    else:
        return "🔴", "Crítico", "#e74c3c"
