# Contribuir para o Personal Finance Manager

Obrigado pelo interesse em contribuir para este projeto! Este documento descreve as convenções e o fluxo de trabalho usados no repositório.

## Requisitos

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) para gestão de dependências e ambiente virtual

## Configuração do ambiente

```bash
# Clonar o repositório
git clone https://github.com/esmeraldafonseca/personal-finance-manager.git
cd personal-finance-manager

# Instalar dependências com uv
uv sync

# Ativar o ambiente virtual
source .venv/bin/activate
```

## Estrutura do projeto

```
personal-finance-manager/
├── main.py                          # Ponto de entrada da aplicação
├── database/
│   └── database.py                  # Configuração e conexão com o SQLite
├── models/
│   └── transaction.py                 # Modelo de dados dos transactions financeiros
├── repositories/
│   └── transaction_repositorio.py     # Camada de acesso a dados
├── services/
│   └── relatorios.py                # Lógica de negócio e geração de relatórios
├── ui/
│   └── interface.py                 # Interface com o utilizador
├── charts/
│   └── grafico.py                   # Geração de gráficos
├── pyproject.toml                   # Dependências e configuração do projeto
└── CONTRIBUTING.md
```

## Fluxo de trabalho com Git

1. Cria um branch a partir de `main` com um nome descritivo:
   - `feature/nome-da-funcionalidade`
   - `fix/nome-do-bug`
   - `refactor/nome-da-parte`
   - `security/descricao-da-correcao`
2. Faz commits pequenos e focados — um commit deve representar uma alteração lógica, não uma mistura de coisas diferentes.
3. Quando terminares, garante que o código corre sem erros antes de fazer merge para `main`.

## Convenção de mensagens de commit

Este projeto segue o padrão de [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>: <descrição curta em minúsculas>
```

Tipos usados:

| Tipo       | Quando usar                                                        |
|------------|---------------------------------------------------------------------|
| `feat`     | Nova funcionalidade                                                 |
| `fix`      | Correção de bug                                                     |
| `refactor` | Reestruturação de código sem alterar comportamento                  |
| `security` | Correções relacionadas com segurança ou validação de dados          |
| `docs`     | Alterações na documentação                                          |
| `chore`    | Tarefas de manutenção (dependências, configuração, etc.)            |
| `test`     | Adição ou alteração de testes                                       |

Exemplos:

```
feat: adiciona filtro de transactions por categoria
fix: corrige cálculo do saldo mensal
security: sanitiza inputs antes de gravar na base de dados
refactor: remove validação redundante no repositório de transactions
docs: atualiza instruções de instalação com uv
```

## Boas práticas de código

- Mantém funções pequenas e com responsabilidade única.
- Evita duplicação de lógica entre `services/` e `repositories/`.
- Valida sempre os dados de entrada antes de os gravar na base de dados.
- Não deixes credenciais, caminhos absolutos ou dados sensíveis no código — usa variáveis de ambiente quando necessário.

## Dependências

Para adicionar uma nova dependência:

```bash
uv add nome-do-pacote
```

Para adicionar uma dependência apenas de desenvolvimento (ex: testes, linters):

```bash
uv add --dev nome-do-pacote
```