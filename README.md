# Personal Finance Manager

Aplicação desktop para gestão de finanças pessoais, desenvolvida em Python com interface gráfica em Flet.

Projeto académico desenvolvido por **Esmeralda Fonseca**, sob orientação do **Prof. Eng. Sebilson Cristovão**.

## Funcionalidades

- **Dashboard** — resumo mensal com total de receitas, despesas, saldo e últimas movimentações.
- **Movimentações** — listagem, pesquisa e filtro de todas as receitas e despesas registadas.
- **Adicionar** — formulário validado para registar novas movimentações.
- **Relatório Mensal** — totais, saldo, maior receita/despesa e categoria com maior despesa.
- **Gráficos** — comparação de receitas vs despesas e distribuição de despesas por categoria.
- **Categorias** — totais acumulados por categoria.

## Stack Tecnológico

| Tecnologia | Função |
|---|---|
| Python 3 | Linguagem base da aplicação |
| Flet | Interface gráfica de secretária |
| SQLite | Base de dados local |
| Matplotlib | Geração dos gráficos financeiros |

## Arquitetura

O projeto está organizado em camadas, dos dados até à interface:

```
Database              → ligação SQLite e criação da tabela 'movimentos'
Transaction           → dataclass com validação e mapeamento de dados
TransactionRepository → operações CRUD, pesquisa, filtros e agregações
FinancialReport       → regras de negócio e cálculo do relatório mensal
charts                → geração dos gráficos (Matplotlib)
app_layout            → sidebar, navegação e estado partilhado entre vistas
views/                → um ficheiro por ecrã (dashboard, movimentações,
                        adicionar, pesquisar, relatórios, gráficos,
                        categorias)
```

## Estrutura do Projeto

```
projecto3-app/
├── database/
│   └── database.py
├── models/
│   └── transaction.py
├── repositories/
│   └── transaction_repository.py
├── services/
│   └── financial_report.py
├── charts/
│   └── charts.py
├── ui/
│   ├── app_layout.py
│   └── views/
│       ├── theme.py
│       ├── dashboard_view.py
│       ├── transactions_view.py
│       ├── add_transaction_view.py
│       ├── search_view.py
│       ├── reports_view.py
│       ├── charts_view.py
│       └── categories_view.py
├── main.py
└── pyproject.toml
```

## Correr a aplicação

Instalar as dependências:

```bash
uv sync
```

Correr como aplicação de secretária:

```bash
uv run flet run
```

Correr como aplicação web:

```bash
uv run flet run --web
```

Para mais detalhes, consulta o [Getting Started Guide](https://flet.dev/docs/) do Flet.

## Melhorias Futuras

- Normalização da categoria numa tabela própria, com chave estrangeira.
- Filtro combinado por múltiplos critérios em simultâneo.
- Testes automatizados.


## 👩‍💻 Autora

**Esmeralda Fonseca**

Projeto académico desenvolvido no âmbito da formação orientada pelo formador **Sebilson Cristóvão**.


## 📄 Contribuições

Contribuições são bem-vindas. Por favor faça um fork do repositorio e envie um pull request com as suas melhorias