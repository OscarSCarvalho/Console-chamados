# Console de Chamados — Athos Tecnologia

Aplicação web interna para gestão de tickets de suporte técnico.
Stack: **Flask + SQLite puro** (sem ORM), sessão nativa do Flask, frontend com Jinja2 + CSS/JS vanilla.

---

## Como rodar

```bash
pip install -r requirements.txt
python seed.py      # cria console.db com dados de exemplo (rodar só uma vez)
python app.py       # inicia em http://localhost:5000
```

## Logins de teste

| E-mail                | Senha       | Papel     |
|-----------------------|-------------|-----------|
| oscar@athos.com.br    | oscar123    | admin     |
| rafael@athos.com.br   | rafael123   | atendente |
| marina@athos.com.br   | marina123   | atendente |

---

## Funcionalidades

### Board Kanban
- Quatro colunas: **Aberto → Em andamento → Aguardando setor → Resolvido**
- Drag-and-drop entre colunas atualiza o status via API JSON
- Clique em qualquer card abre a página de detalhe do chamado

### Detalhe do chamado
- Descrição completa do chamado
- **Timeline unificada**: movimentações de status e comentários em ordem cronológica
- Formulário de comentário embutido na timeline
- Sidebar com seletor de status, seletor de atribuição e barra de SLA
- Exclusão de chamado (somente admin), com confirmação

### KPIs em tempo real (6 cards)
| KPI | Descrição |
|-----|-----------|
| Total ativos | Chamados abertos + andamento + aguardando |
| Em andamento | Chamados na coluna "andamento" |
| Aguardando setor | Chamados aguardando resposta interna |
| SLA em risco | Chamados com SLA ≥ 75% consumido |
| MTTR (30 dias) | Tempo médio de resolução em horas (últimos 30 dias) |
| SLA cumprido | % de chamados resolvidos dentro do prazo histórico |

### SLA automático por prioridade
| Prioridade | SLA padrão |
|------------|------------|
| Alta       | 4h         |
| Média      | 24h        |
| Baixa      | 48h        |

A barra de progresso muda de cor: verde (< 40%), âmbar (40–75%), vermelho (> 75% ou vencido).

### Exportação CSV
Botão `↓` na topbar exporta todos os chamados com 12 colunas (ID, título, descrição, prioridade, status, SLA, setor, atribuído, criado por, datas).

### Gestão de usuários (somente admin)
- Ícone 👥 na topbar abre `/usuarios`
- Criar, editar (nome, papel, senha opcional) e ativar/desativar contas
- Contador de chamados ativos por atendente

---

## Estrutura do projeto

```
console-chamados/
├── app.py                  # rotas Flask, lógica de SLA, autenticação
├── schema.sql              # DDL das 5 tabelas
├── seed.py                 # cria o banco e popula com dados de exemplo
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── board.html          # Kanban + KPIs
│   ├── chamado_detalhe.html # detalhe, timeline e comentários
│   └── usuarios.html       # CRUD de usuários (admin)
└── static/
    ├── css/style.css       # tema navy/amber
    └── js/board.js         # drag-and-drop + navegação por clique
```

## Banco de dados

```
usuarios      — contas (atendente / admin), hash bcrypt
setores       — departamentos vinculados aos chamados
chamados      — ticket principal (título, descrição, prioridade, status, SLA)
movimentacoes — auditoria de cada mudança de status
comentarios   — anotações internas por chamado
```

> O banco (`console.db`) é gerado localmente e **não é versionado**.

## Rotas principais

| Rota | Método | Acesso | Descrição |
|------|--------|--------|-----------|
| `/login` | GET/POST | público | Autenticação |
| `/logout` | GET | autenticado | Encerra sessão |
| `/` | GET | autenticado | Board Kanban |
| `/chamados` | POST | autenticado | Cria chamado |
| `/chamados/exportar` | GET | autenticado | Download CSV |
| `/chamados/<id>` | GET | autenticado | Detalhe do chamado |
| `/chamados/<id>/comentarios` | POST | autenticado | Adiciona comentário |
| `/chamados/<id>/status` | POST | autenticado | Atualiza status (JSON) |
| `/chamados/<id>/atribuir` | POST | autenticado | Atribui responsável (JSON) |
| `/chamados/<id>` | DELETE | admin | Exclui chamado |
| `/usuarios` | GET | admin | Lista usuários |
| `/usuarios` | POST | admin | Cria usuário |
| `/usuarios/<id>/editar` | POST | admin | Edita usuário |
| `/usuarios/<id>/toggle` | POST | admin | Ativa/desativa usuário |

## Decisões de arquitetura

- **Sem SQLAlchemy** — `sqlite3` puro, mais simples para um app interno de escopo controlado.
- **Sem JWT** — sessão nativa do Flask é suficiente para uso interno.
- **Sem WebSocket** — atualização via reload após ação: simples e previsível.
- **Migração automática** — `migrate_db()` em `app.py` cria tabelas novas em bancos existentes sem apagar dados.
- **SLA fixo por prioridade** — para SLA por setor, basta adicionar `sla_padrao_horas` na tabela `setores`.
