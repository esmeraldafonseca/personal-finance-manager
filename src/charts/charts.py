import io

import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt

# Paleta de cores 
INCOME_COLOR = "#1F6F63"
EXPENSE_COLOR = "#F4B400"
TEXT_COLOR = "#0D2B2E"
CATEGORY_COLORS = [
    "#0D2B2E",
    "#1F6F63", 
    "#4CAF87", 
    "#BFE3D1", 
    "#F4B400", 
    "#8FD9BE", 
    "#2E8B74", 
    "#D9A400"]


class NoChartDataError(Exception):
    """Lançado quando não existem dados suficientes para gerar um gráfico."""


def _figure_to_bytes(fig) -> bytes:
    """Converte uma figura matplotlib em bytes PNG, prontos para o controlo ft.Image."""
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=130, transparent=True)
    plt.close(fig)
    buffer.seek(0)
    return buffer.read()


def income_vs_expenses_chart(total_income: float, total_expenses: float) -> bytes:
    """
    Gera um gráfico de barras comparando o total de receitas com o
    total de despesas. Devolve os bytes PNG da imagem.
    """
    if total_income <= 0 and total_expenses <= 0:
        raise NoChartDataError("Não existem dados suficientes para gerar o gráfico.")

    fig, ax = plt.subplots(figsize=(5.5, 4))
    labels = ["Receitas", "Despesas"]
    values = [total_income, total_expenses]
    colors = [INCOME_COLOR, EXPENSE_COLOR]

    bars = ax.bar(labels, values, color=colors, width=0.5)

    ax.set_title("Receitas vs Despesas", fontsize=13, fontweight="bold", color=TEXT_COLOR)
    ax.set_ylabel("Valor (Kz)", color=TEXT_COLOR)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=TEXT_COLOR)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,.2f} Kz",
            ha="center", va="bottom", fontsize=9, color=TEXT_COLOR,
        )

    fig.tight_layout()
    return _figure_to_bytes(fig)


def expenses_by_category_chart(data: list) -> bytes:
    """
    Gera um gráfico circular (pizza) com a distribuição das despesas por
    categoria. 'data' é uma lista de tuplos (categoria, total), tal como
    devolvida por TransactionRepository.totals_by_category().
    """
    valid_data = [(category, total) for category, total in data if total and total > 0]

    if not valid_data:
        raise NoChartDataError("Não existem despesas suficientes para gerar o gráfico.")

    categories = [item[0] for item in valid_data]
    values = [item[1] for item in valid_data]
    colors = (CATEGORY_COLORS * ((len(categories) // len(CATEGORY_COLORS)) + 1))[: len(categories)]

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    wedges, _, autotexts = ax.pie(
        values,
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%" if pct >= 3 else "",
        startangle=90,
        colors=colors,
        pctdistance=0.8,
        wedgeprops={"width": 0.4, "edgecolor": "white"},
    )
    for text in autotexts:
        text.set_color("white")
        text.set_fontsize(8)
        text.set_fontweight("bold")

    ax.set_title("Despesas por Categoria", fontsize=13, fontweight="bold", color=TEXT_COLOR)
    ax.legend(
        wedges, categories, title="Categorias", loc="center left",
        bbox_to_anchor=(1.0, 0.5), fontsize=8, frameon=False,
    )
    ax.axis("equal")

    fig.tight_layout()
    return _figure_to_bytes(fig)