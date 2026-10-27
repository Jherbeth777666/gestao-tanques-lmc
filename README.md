# PostoControl AI — gestão de tanques e LMC para postos de combustível

Sistema web que converte a medição da régua (cm) em litros, fecha o Livro de Movimentação de Combustíveis (LMC) do dia e verifica se a perda ou sobra está dentro da tolerância de ±0,6% da ANP.

## Problema

No posto, o fechamento diário depende de contas feitas à mão:

- converter a altura medida na régua em litros, tanque por tanque;
- calcular o estoque escritural (inicial + recebimentos − vendas nos bicos);
- comparar com o estoque físico e decidir se a variação exige providência.

Cálculo manual é lento e sujeito a erro justamente na conta que vai para o LMC.

## Solução

| Etapa | O que o sistema faz |
|---|---|
| Medição | Converte a régua em litros pela geometria de tanque cilíndrico horizontal (arqueação), para tanques de 7.500 a 20.000 L |
| Encerrantes | Calcula as vendas a partir da leitura inicial e final de cada bico |
| Fechamento do LMC | Estoque escritural, perda/sobra em litros e em %, e status ANP: conforme, perda excessiva ou sobra excessiva |
| Histórico | Guarda cada fechamento por tanque e data |
| Parecer com IA | Envia os números do fechamento ao Gemini e devolve diagnóstico, risco e ações recomendadas; sem chave de API, responde com uma análise padrão |

## Tecnologias

Python · FastAPI · SQLAlchemy · PostgreSQL (Supabase) · Pydantic · HTML/CSS/JavaScript · Google Gemini · pytest

## Segurança

- Login com token assinado (HMAC-SHA256) e validade de 12 horas.
- Todas as rotas de dados exigem o token; sem login, a API responde 401.
- Nenhuma senha no código: sem `ADMIN_PASSWORD` definida, o login fica desabilitado.
- CORS fechado por padrão, liberado só para as origens listadas.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Variáveis de ambiente:

| Variável | Obrigatória | Uso |
|---|---|---|
| `DATABASE_URL` | sim | Conexão com o PostgreSQL |
| `ADMIN_PASSWORD` | sim | Senha de acesso ao sistema |
| `ADMIN_USER` | não | Usuário de acesso (padrão: `admin`) |
| `SECRET_KEY` | recomendada | Chave que assina os tokens; sem ela, as sessões caem a cada reinício |
| `GEMINI_API_KEY` | não | Ativa o parecer com IA |
| `ALLOWED_ORIGINS` | não | Origens liberadas no CORS, separadas por vírgula |

## Testes

```bash
pip install pytest httpx
python -m pytest
```

## Próximos passos

- Tabela de arqueação oficial de cada tanque no lugar da fórmula geométrica.
- Exportação do LMC em PDF.
- Mais de um usuário, com perfis de acesso.
