import os
import json
import urllib.request
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/ia", tags=["Inteligência Artificial"])

class AuditoriaRequest(BaseModel):
    tanque: str
    combustivel: str
    capacidade: float
    data_movimento: str
    estoque_inicial: float
    recebimentos: float
    vendas: float
    estoque_escritural: float
    estoque_fisico: float
    perda_sobra: float
    percentual_variacao: float
    status_anp: str

def chamar_gemini(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return ""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 800}
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"[Aviso Gemini] {e}")
        return ""

@router.post("/auditar")
def auditar_fechamento(req: AuditoriaRequest):
    prompt = f"""
Você é um auditor especialista em regulamentação da ANP e engenharia de postos de combustíveis no Brasil.
Analise os seguintes dados do fechamento diário do LMC:

- Tanque: {req.tanque} ({req.combustivel}, Capacidade Máxima: {req.capacidade:,.0f} L)
- Data do Movimento: {req.data_movimento}
- Estoque Inicial: {req.estoque_inicial:,.1f} L
- Recebimentos (NF-e): {req.recebimentos:,.1f} L
- Vendas Totais nos Bicos: {req.vendas:,.1f} L
- Estoque Escritural Calculado: {req.estoque_escritural:,.1f} L
- Estoque Físico Aferido na Régua: {req.estoque_fisico:,.1f} L
- Variação Diária: {req.perda_sobra:,.1f} L ({req.percentual_variacao:+.3f}%)
- Limite Regulamentar ANP: Margem máxima de tolerância de ±0,6%.
- Status do Sistema: {req.status_anp}

Estruture sua resposta estritamente no seguinte padrão:
1. 🔍 Diagnóstico Físico & Operacional
2. ⚠️ Classificação de Risco
3. 🛠️ Ações Imediatas Recomendadas
4. 📋 Parecer Técnico para o LMC
"""

    resposta_gemini = chamar_gemini(prompt)

    if not resposta_gemini:
        sinal = "+" if req.perda_sobra > 0 else ""
        if req.status_anp == "CONFORME":
            resposta_gemini = f"""### 🔍 Diagnóstico Físico & Operacional
A variação de **{sinal}{req.perda_sobra:.1f} L ({req.percentual_variacao:+.3f}%)** para o produto **{req.combustivel}** está plenamente dentro dos padrões de tolerância admitidos pela Portaria DNC 26 / Resolução ANP (limite legal de ±0,600%). Flutuações dessa magnitude são naturais em tanques subterrâneos devido à estabilização térmica do combustível e perdas normais por volatilidade.

### ⚠️ Classificação de Risco
**NÍVEL BAIXO (Operação Regular)**.

### 🛠️ Ações Imediatas Recomendadas
1. Manter a rotina padrão de aferição matinal da régua no mesmo horário para evitar variações de temperatura externa.
2. Validar se os encerrantes das bombas conferem com o relatório do sistema de automação comercial.

### 📋 Parecer Técnico para o LMC
"Movimentação encerrada em conformidade com as normas da ANP. Variação volumétrica de {req.percentual_variacao:+.3f}% decorrente de acomodação térmica natural do produto, sem anomalias operacionais registradas."
"""
        else:
            resposta_gemini = f"""### 🔍 Diagnóstico Físico & Operacional
🚨 **Atenção:** A variação de **{sinal}{req.perda_sobra:.1f} L ({req.percentual_variacao:+.3f}%)** extrapolou a margem regulamentar de **±0,6%** da ANP. No caso de perda acentuada em {req.combustivel}, deve-se descartar erro de leitura da régua antes de investigar descalibração do medidor volumétrico do bico ou anomalia nas tubulações.

### ⚠️ Classificação de Risco
**NÍVEL CRÍTICO (Risco de Autuação Fiscal / Perda Financeira)**.

### 🛠️ Ações Imediatas Recomendadas
1. **Realizar contraprova imediata:** Efetuar nova medição física da régua com pasta d'água para confirmar presença de água ou erro de leitura.
2. **Aferição com balde aferidor de 20L:** Aferir os bicos conectados a este tanque para verificar se as bombas não estão a entregar volume acima do registado.
3. Registar a ocorrência no livro e monitorizar as próximas 24 horas para descartar fugas em linha.

### 📋 Parecer Técnico para o LMC
"Variação fora do padrão de 0,6% identificada no fechamento diário. Procedimento de aferição dos bicos de abastecimento e contraprova física da régua instaurados imediatamente para apuração e correção técnica."
"""

    return {"parecer_ia": resposta_gemini}
