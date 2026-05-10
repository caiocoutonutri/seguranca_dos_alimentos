# modules/formulario.py
# Checklist de Visita Técnica — Consultoria Mariner
# RDC 216 · Segurança dos Alimentos
# Vocabulário simplificado para uso em campo (mobile-friendly)
#
# ORDEM DAS SEÇÕES: fluxo natural da visita técnica do nutricionista
# 1. Higiene Pessoal (primeiro contato com equipe)
# 2. Armazenamento Geral (validade, etiquetas)
# 3. Pré-Preparo e Preparo (produção)
# 4. Móveis, Equipamentos e Utensílios (estado geral)
# 5. Higienização Ambiental (limpeza de superfícies)
# 6. Congelados e Refrigerados (temperaturas)
# 7. Controle de Pragas (inspeção visual)
# 8. Registros e Documentação (papelada)
# 9. Vestiários e Sanitários (dependências)
# 10. Estoque Seco (produtos secos)
# 11. Abastecimento de Água (laudos)
# 12. Esgoto e Descarte de Óleo
# 13. Produtos de Limpeza (químicos)
# 14. Estrutura Física (instalações)
# 15. Lixo e Resíduos
# 16. Coleta de Amostras
# 17. Manutenção e Climatização

SECOES = [
    # ──────────────────────────────────────────────
    # SEÇÃO 1 — HIGIENE PESSOAL (70 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 1,
        "titulo": "Higiene Pessoal",
        "pontuacao_maxima": 70,
        "perguntas": [
            {
                "id": "1.1",
                "texto": "Pia para lavar as mãos está livre e acessível",
                "pontos": 4,
            },
            {
                "id": "1.2",
                "texto": "Pia equipada com sabonete bactericida, papel toalha descartável e cartaz de orientação",
                "pontos": 8,
            },
            {
                "id": "1.3",
                "texto": "Funcionários lavam as mãos corretamente e com frequência",
                "pontos": 40,
            },
            {
                "id": "1.4",
                "texto": "Uniformes completos, limpos e em bom estado",
                "pontos": 4,
            },
            {
                "id": "1.5",
                "texto": "EPIs em uso, limpos e em quantidade suficiente",
                "pontos": 2,
            },
            {
                "id": "1.6",
                "texto": "Cabelos protegidos com touca/rede; barba feita ou com protetor",
                "pontos": 2,
            },
            {
                "id": "1.7",
                "texto": "Sem adornos, maquiagem, esmalte ou perfume",
                "pontos": 4,
            },
            {
                "id": "1.8",
                "texto": "Unhas curtas e limpas; sem feridas, cortes ou infecções visíveis",
                "pontos": 6,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 2 — ARMAZENAMENTO GERAL (60 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 2,
        "titulo": "Armazenamento Geral",
        "pontuacao_maxima": 60,
        "perguntas": [
            {
                "id": "2.1",
                "texto": "Sistema PVPS aplicado — Primeiro que Vence, Primeiro que Sai",
                "pontos": 4,
            },
            {
                "id": "2.2",
                "texto": "Produtos abertos, transferidos ou em descongelamento estão identificados corretamente",
                "pontos": 6,
            },
            {
                "id": "2.3",
                "texto": "Etiquetas preenchidas com data de abertura e nova validade",
                "pontos": 4,
            },
            {
                "id": "2.4",
                "texto": "Nenhum produto vencido no estoque ou área de produção",
                "pontos": 40,
            },
            {
                "id": "2.5",
                "texto": "Produtos impróprios ou para descarte estão separados e identificados",
                "pontos": 6,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 3 — PRÉ-PREPARO E PREPARO (110 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 3,
        "titulo": "Pré-Preparo e Preparo",
        "pontuacao_maxima": 110,
        "perguntas": [
            {
                "id": "3.1",
                "texto": "Medidas para evitar contaminação cruzada estão sendo seguidas",
                "pontos": 40,
            },
            {
                "id": "3.2",
                "texto": "Sem risco de contaminação física ou química nos alimentos",
                "pontos": 4,
            },
            {
                "id": "3.3",
                "texto": "Bons hábitos: ninguém coça, espirra, tosse ou come sobre os alimentos",
                "pontos": 6,
            },
            {
                "id": "3.4",
                "texto": "Alimentos protegidos (cobertos/tampados) durante o preparo",
                "pontos": 4,
            },
            {
                "id": "3.5",
                "texto": "Descongelamento feito corretamente; nada é recongelado após descongelar",
                "pontos": 8,
            },
            {
                "id": "3.6",
                "texto": "Frutas, legumes e verduras (FLV) higienizados adequadamente",
                "pontos": 8,
            },
            {
                "id": "3.7",
                "texto": "Perecíveis fora da refrigeração por no máximo 30 min (ou 2h se climatizado)",
                "pontos": 8,
            },
            {
                "id": "3.8",
                "texto": "Cocção e reaquecimento atingem ≥ 74°C no centro do alimento",
                "pontos": 8,
            },
            {
                "id": "3.9",
                "texto": "Resfriamento feito de forma rápida e segura",
                "pontos": 8,
            },
            {
                "id": "3.10",
                "texto": "Óleo de fritura com cor, cheiro e temperatura adequados",
                "pontos": 4,
            },
            {
                "id": "3.11",
                "texto": "Alimentos em espera mantidos quentes ou refrigerados — nunca em temperatura ambiente",
                "pontos": 8,
            },
            {
                "id": "3.12",
                "texto": "Banho-maria, estufas e pass-through em temperatura correta",
                "pontos": 4,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 4 — MÓVEIS, EQUIPAMENTOS E UTENSÍLIOS (12 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 4,
        "titulo": "Móveis, Equipamentos e Utensílios",
        "pontuacao_maxima": 12,
        "perguntas": [
            {
                "id": "4.1",
                "texto": "Armários, prateleiras, bancadas e pallets em bom estado",
                "pontos": 2,
            },
            {
                "id": "4.2",
                "texto": "Câmaras frias e equipamentos de refrigeração/congelamento em bom estado",
                "pontos": 4,
            },
            {
                "id": "4.3",
                "texto": "Equipamentos que NÃO tocam alimentos em bom estado (ex: coifas, estantes)",
                "pontos": 2,
            },
            {
                "id": "4.4",
                "texto": "Equipamentos e utensílios que TOCAM alimentos em bom estado (ex: facas, tábuas, cubas)",
                "pontos": 4,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 5 — HIGIENIZAÇÃO AMBIENTAL (70 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 5,
        "titulo": "Higienização Ambiental",
        "pontuacao_maxima": 70,
        "perguntas": [
            {
                "id": "5.1",
                "texto": "Piso, paredes, teto e áreas comuns estão limpos",
                "pontos": 4,
            },
            {
                "id": "5.2",
                "texto": "Câmaras frias e equipamentos de refrigeração estão limpos por dentro e por fora",
                "pontos": 4,
            },
            {
                "id": "5.3",
                "texto": "Móveis e equipamentos SEM contato com alimentos estão limpos (estantes, parte de baixo de bancadas)",
                "pontos": 4,
            },
            {
                "id": "5.4",
                "texto": "Superfícies e utensílios COM contato direto com alimentos estão limpos e sanitizados",
                "pontos": 40,
            },
            {
                "id": "5.5",
                "texto": "Utensílios e equipamentos higienizados guardados em local adequado",
                "pontos": 6,
            },
            {
                "id": "5.6",
                "texto": "Processo de higienização correto: lavar → enxaguar → desinfetar → enxaguar novamente",
                "pontos": 8,
            },
            {
                "id": "5.7",
                "texto": "Nenhum alimento armazenado em contato direto com o piso",
                "pontos": 4,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 6 — CONGELADOS E REFRIGERADOS (20 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 6,
        "titulo": "Congelados e Refrigerados",
        "pontuacao_maxima": 20,
        "perguntas": [
            {
                "id": "6.1",
                "texto": "Produtos organizados por categoria, com espaçamento entre eles",
                "pontos": 4,
            },
            {
                "id": "6.2",
                "texto": "Freezers em temperatura adequada (≤ −18°C)",
                "pontos": 8,
            },
            {
                "id": "6.3",
                "texto": "Geladeiras/câmaras em temperatura adequada (≤ 5°C)",
                "pontos": 8,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 7 — CONTROLE DE PRAGAS (54 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 7,
        "titulo": "Controle de Pragas",
        "pontuacao_maxima": 54,
        "perguntas": [
            {
                "id": "7.1",
                "texto": "Sem ratos ou baratas (vivas ou mortas) no estabelecimento",
                "pontos": 40,
            },
            {
                "id": "7.2",
                "texto": "Sem insetos voadores, formigas ou outras pragas",
                "pontos": 6,
            },
            {
                "id": "7.3",
                "texto": "Sem infestação de drosófilas (mosquitinhos de fruta)",
                "pontos": 2,
            },
            {
                "id": "7.4",
                "texto": "Barreiras físicas funcionando: telas, vedações em portas, ralos protegidos",
                "pontos": 6,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 8 — REGISTROS E DOCUMENTAÇÃO (56 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 8,
        "titulo": "Registros e Documentação",
        "pontuacao_maxima": 56,
        "perguntas": [
            {
                "id": "8.1",
                "texto": "Planilha de temperatura e rastreabilidade no recebimento de perecíveis",
                "pontos": 6,
            },
            {
                "id": "8.2",
                "texto": "Planilha de rastreabilidade no recebimento de produtos secos",
                "pontos": 2,
            },
            {
                "id": "8.3",
                "texto": "Planilha de temperatura das geladeiras e freezers",
                "pontos": 6,
            },
            {
                "id": "8.4",
                "texto": "Planilha de temperatura dos equipamentos de manutenção (banho-maria, estufa) e alimentos em espera",
                "pontos": 6,
            },
            {
                "id": "8.5",
                "texto": "Planilha de temperatura dos equipamentos na distribuição",
                "pontos": 4,
            },
            {
                "id": "8.6",
                "texto": "Planilha de temperatura dos alimentos na distribuição",
                "pontos": 6,
            },
            {
                "id": "8.7",
                "texto": "Registro da concentração do sanitizante usado na higienização de FLV",
                "pontos": 6,
            },
            {
                "id": "8.8",
                "texto": "Registro de controle do óleo de fritura",
                "pontos": 6,
            },
            {
                "id": "8.9",
                "texto": "Registro de higienização de instalações, móveis, equipamentos e utensílios",
                "pontos": 6,
            },
            {
                "id": "8.10",
                "texto": "Registro de treinamento dos funcionários em Boas Práticas (BPF)",
                "pontos": 8,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 9 — VESTIÁRIOS E SANITÁRIOS (10 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 9,
        "titulo": "Vestiários e Sanitários",
        "pontuacao_maxima": 10,
        "perguntas": [
            {
                "id": "9.1",
                "texto": "Vestiários e banheiros em bom estado de conservação",
                "pontos": 2,
            },
            {
                "id": "9.2",
                "texto": "Vestiários e banheiros limpos e organizados",
                "pontos": 2,
            },
            {
                "id": "9.3",
                "texto": "Vestiários com sabonete bactericida, papel toalha, lixeira com pedal e cartaz de higienização",
                "pontos": 6,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 10 — ESTOQUE SECO (8 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 10,
        "titulo": "Estoque Seco",
        "pontuacao_maxima": 8,
        "perguntas": [
            {
                "id": "10.1",
                "texto": "Produtos organizados por categoria, com espaçamento adequado",
                "pontos": 2,
            },
            {
                "id": "10.2",
                "texto": "Alimentos separados dos produtos químicos e embalagens descartáveis",
                "pontos": 6,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 11 — ABASTECIMENTO DE ÁGUA (30 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 11,
        "titulo": "Abastecimento de Água",
        "pontuacao_maxima": 30,
        "perguntas": [
            {
                "id": "11.1",
                "texto": "Certificado de limpeza da caixa d'água atualizado (semestral)",
                "pontos": 8,
            },
            {
                "id": "11.2",
                "texto": "Registro de troca dos filtros de água com etiqueta e nota fiscal",
                "pontos": 6,
            },
            {
                "id": "11.3",
                "texto": "Água da rede pública: laudo de potabilidade atualizado",
                "pontos": 8,
            },
            {
                "id": "11.4",
                "texto": "Água de poço ou fonte alternativa: laudo de potabilidade atualizado",
                "pontos": 8,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 12 — ESGOTO E DESCARTE DE ÓLEO (20 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 12,
        "titulo": "Esgoto e Descarte de Óleo",
        "pontuacao_maxima": 20,
        "perguntas": [
            {
                "id": "12.1",
                "texto": "Caixa de gordura em bom estado e limpa",
                "pontos": 4,
            },
            {
                "id": "12.2",
                "texto": "Registro de limpeza da caixa de gordura atualizado",
                "pontos": 4,
            },
            {
                "id": "12.3",
                "texto": "Óleo usado NÃO é jogado no ralo — está guardado em galões para coleta",
                "pontos": 6,
            },
            {
                "id": "12.4",
                "texto": "Comprovantes de coleta do óleo usado disponíveis",
                "pontos": 4,
            },
            {
                "id": "12.5",
                "texto": "Galões de óleo para descarte armazenados com contenção, fora da produção e identificados",
                "pontos": 2,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 13 — PRODUTOS DE LIMPEZA (10 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 13,
        "titulo": "Produtos de Limpeza",
        "pontuacao_maxima": 10,
        "perguntas": [
            {
                "id": "13.1",
                "texto": "Produtos químicos com registro na ANVISA, identificados e dentro da validade",
                "pontos": 4,
            },
            {
                "id": "13.2",
                "texto": "Fichas técnicas e fichas de segurança dos produtos disponíveis",
                "pontos": 2,
            },
            {
                "id": "13.3",
                "texto": "Materiais de limpeza (esponjas, panos, rodos) em bom estado e limpos",
                "pontos": 4,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 14 — ESTRUTURA FÍSICA (18 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 14,
        "titulo": "Estrutura Física",
        "pontuacao_maxima": 18,
        "perguntas": [
            {
                "id": "14.1",
                "texto": "Pisos íntegros, sem rachaduras ou buracos",
                "pontos": 2,
            },
            {
                "id": "14.2",
                "texto": "Ralos limpos, com tampa e funcionando",
                "pontos": 2,
            },
            {
                "id": "14.3",
                "texto": "Paredes íntegras e de fácil higienização",
                "pontos": 2,
            },
            {
                "id": "14.4",
                "texto": "Tetos, forros e luminárias em bom estado e com proteção",
                "pontos": 2,
            },
            {
                "id": "14.5",
                "texto": "Torneiras, pias e encanamentos funcionando e em bom estado",
                "pontos": 2,
            },
            {
                "id": "14.6",
                "texto": "Ventilação e exaustão adequadas (sem calor excessivo, sem odores)",
                "pontos": 8,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 15 — LIXO E RESÍDUOS (16 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 15,
        "titulo": "Lixo e Resíduos",
        "pontuacao_maxima": 16,
        "perguntas": [
            {
                "id": "15.1",
                "texto": "Lixo externo em área isolada, fechada e limpa",
                "pontos": 4,
            },
            {
                "id": "15.2",
                "texto": "Lixeiras internas com tampa de pedal, sacos plásticos e limpas",
                "pontos": 6,
            },
            {
                "id": "15.3",
                "texto": "Lixo retirado com frequência das áreas de manipulação e estoque",
                "pontos": 6,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 16 — COLETA DE AMOSTRAS (12 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 16,
        "titulo": "Coleta de Amostras",
        "pontuacao_maxima": 12,
        "perguntas": [
            {
                "id": "16.1",
                "texto": "Método de coleta de amostras está correto",
                "pontos": 4,
            },
            {
                "id": "16.2",
                "texto": "Amostras guardadas por 72h sob refrigeração adequada",
                "pontos": 6,
            },
            {
                "id": "16.3",
                "texto": "Amostras identificadas com data, horário e responsável",
                "pontos": 2,
            },
        ],
    },
    # ──────────────────────────────────────────────
    # SEÇÃO 17 — MANUTENÇÃO E CLIMATIZAÇÃO (6 pts)
    # ──────────────────────────────────────────────
    {
        "numero": 17,
        "titulo": "Manutenção e Climatização",
        "pontuacao_maxima": 6,
        "perguntas": [
            {
                "id": "17.1",
                "texto": "Comprovantes de limpeza, manutenção e troca de filtros do ar-condicionado disponíveis",
                "pontos": 6,
            },
        ],
    },
 ]


# ──────────────────────────────────────────────────
# CONFIGURAÇÕES GERAIS
# ──────────────────────────────────────────────────

OPCOES_RESPOSTA = [
    "Selecione...",
    "Conforme",
    "Não Conforme",
    "Não Aplicável",
]

UNIDADES = [
    "Selecione a unidade...",
    "Mariner",
    "Praiano",
    "Quim",
    "Buonasera",
    "Anexo",
]

Responsaveis = [
    "Selecione o responsável...",
    "Andre",
    "Rainnie",
    "Bruno",
    "Sandro",
    "Lucas",
]

Nutricionistas = [
    "Caio Couto",
]


# ──────────────────────────────────────────────────
# FUNÇÕES DE CÁLCULO
# ──────────────────────────────────────────────────

def classificar_nota(percentual):
    """
    Retorna emoji, label e cor baseado no percentual de conformidade.
    
    Faixas:
        ≥ 90%        → Verde escuro  | Excelente
        80% a 89.99% → Verde         | Bom
        70% a 79.99% → Amarelo       | Atenção
        < 70%        → Vermelho      | Crítico
    """
    if percentual >= 90:
        return "🟩", "Excelente", "#1a5e1a"
    elif percentual >= 80:
        return "🟢", "Bom", "#27ae60"
    elif percentual >= 70:
        return "🟡", "Atenção", "#f39c12"
    else:
        return "🔴", "Crítico", "#e74c3c"


def calcular_pontuacao(respostas):
    """
    Recebe dict de respostas {id_pergunta: resposta} e retorna resumo completo.

    Retorna dict com:
        - secoes: lista com pontuação por seção (obtido, máximo, %)
        - total_obtido: soma total de pontos conquistados
        - total_maximo: soma total possível (descontando NA)
        - percentual: nota geral em %
        - classificacao: (emoji, label, cor)
        - nao_conformidades: lista de itens reprovados
    """
    resultado_secoes = []
    total_obtido = 0
    total_maximo = 0
    nao_conformidades = []

    for secao in SECOES:
        secao_obtido = 0
        secao_maximo = 0

        for pergunta in secao["perguntas"]:
            resposta = respostas.get(pergunta["id"], "Selecione...")

            if resposta == "Conforme":
                secao_obtido += pergunta["pontos"]
                secao_maximo += pergunta["pontos"]
            elif resposta == "Não Conforme":
                secao_maximo += pergunta["pontos"]
                nao_conformidades.append({
                    "secao": secao["titulo"],
                    "secao_numero": secao["numero"],
                    "id": pergunta["id"],
                    "texto": pergunta["texto"],
                    "pontos_perdidos": pergunta["pontos"],
                })
            elif resposta == "Não Aplicável":
                pass  # NA não entra no cálculo

        pct = (secao_obtido / secao_maximo * 100) if secao_maximo > 0 else 100.0

        resultado_secoes.append({
            "numero": secao["numero"],
            "titulo": secao["titulo"],
            "obtido": secao_obtido,
            "maximo": secao_maximo,
            "percentual": round(pct, 1),
        })

        total_obtido += secao_obtido
        total_maximo += secao_maximo

    pct_geral = (total_obtido / total_maximo * 100) if total_maximo > 0 else 100.0

    return {
        "secoes": resultado_secoes,
        "total_obtido": total_obtido,
        "total_maximo": total_maximo,
        "percentual": round(pct_geral, 1),
        "classificacao": classificar_nota(pct_geral),
        "nao_conformidades": nao_conformidades,
    }


# ──────────────────────────────────────────────────
# VERIFICAÇÃO
# ──────────────────────────────────────────────────

TOTAL_PERGUNTAS = sum(len(s["perguntas"]) for s in SECOES)
TOTAL_PONTOS = sum(s["pontuacao_maxima"] for s in SECOES)

if __name__ == "__main__":
    print(f"{'='*65}")
    print(f"  CHECKLIST DE VISITA TÉCNICA — MARINER")
    print(f"  RDC 216 · Segurança dos Alimentos")
    print(f"{'='*65}")
    print(f"  Seções: {len(SECOES)}  |  Perguntas: {TOTAL_PERGUNTAS}  |  Pontuação máx: {TOTAL_PONTOS} pts")
    print(f"{'='*65}")
    print()
    for s in SECOES:
        print(f"  {s['numero']:>2}. {s['titulo']:<42} | {len(s['perguntas']):>2} perguntas | {s['pontuacao_maxima']:>3} pts")
    print()
    print(f"{'='*65}")
