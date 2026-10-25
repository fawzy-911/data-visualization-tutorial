"""Create matching Matplotlib and Seaborn charts from Seaborn's Tips dataset."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


CHARTS_DIR = Path("outputs")
PALETTE = "crest"


def load_tips() -> pd.DataFrame:
    """Load the example dataset distributed through Seaborn's dataset repository."""
    tips = sns.load_dataset("tips")
    if tips.empty:
        raise ValueError("The Tips dataset loaded, but it contains no rows.")
    return tips


def create_matplotlib_charts(tips: pd.DataFrame, output_dir: Path = CHARTS_DIR) -> list[Path]:
    """Create the required five charts with Matplotlib's plotting API."""
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    color = "#287C8E"
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(tips["total_bill"], bins=20, color=color, edgecolor="white")
    ax.set(title="Distribution of Total Bills — Matplotlib", xlabel="Total bill (USD)", ylabel="Number of meals")
    saved.append(_save(fig, output_dir / "matplotlib_histogram.png"))

    grouped = tips.groupby("day", observed=True)["tip"].mean().reindex(["Thur", "Fri", "Sat", "Sun"])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(grouped.index.astype(str), grouped.values, color=["#3B7A8A", "#61A6A8", "#8BBF9F", "#BEDC9A"])
    ax.set(title="Average Tip by Day — Matplotlib", xlabel="Day", ylabel="Average tip (USD)")
    saved.append(_save(fig, output_dir / "matplotlib_bar_chart.png"))

    days = ["Thur", "Fri", "Sat", "Sun"]
    box_data = [tips.loc[tips["day"] == day, "total_bill"].dropna() for day in days]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(box_data, patch_artist=True,
               boxprops={"facecolor": "#8BBF9F", "alpha": 0.8}, medianprops={"color": "#173F43"})
    ax.set_xticks(range(1, len(days) + 1), labels=days)
    ax.set(title="Total Bill by Day — Matplotlib", xlabel="Day", ylabel="Total bill (USD)")
    saved.append(_save(fig, output_dir / "matplotlib_box_plot.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    for smoker, group in tips.groupby("smoker", observed=True):
        ax.scatter(group["total_bill"], group["tip"], label=f"Smoker: {smoker}", alpha=0.72, s=42)
    ax.set(title="Tip vs. Total Bill — Matplotlib", xlabel="Total bill (USD)", ylabel="Tip (USD)")
    ax.legend(title="Table")
    saved.append(_save(fig, output_dir / "matplotlib_scatter_plot.png"))

    corr = tips.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(corr, cmap="YlGnBu", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)), labels=corr.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(corr.index)), labels=corr.index)
    for row in range(len(corr.index)):
        for col in range(len(corr.columns)):
            ax.text(col, row, f"{corr.iloc[row, col]:.2f}", ha="center", va="center", color="#102A2B")
    fig.colorbar(image, ax=ax, label="Correlation")
    ax.set_title("Numeric Feature Correlations — Matplotlib")
    saved.append(_save(fig, output_dir / "matplotlib_heatmap.png"))
    return saved


def create_seaborn_charts(tips: pd.DataFrame, output_dir: Path = CHARTS_DIR) -> list[Path]:
    """Create equivalent charts with Seaborn's higher-level plotting API."""
    output_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    sns.set_theme(style="whitegrid", context="notebook", palette=PALETTE)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=tips, x="total_bill", bins=20, color="#287C8E", ax=ax)
    ax.set(title="Distribution of Total Bills — Seaborn", xlabel="Total bill (USD)", ylabel="Number of meals")
    saved.append(_save(fig, output_dir / "seaborn_histogram.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=tips, x="day", y="tip", order=["Thur", "Fri", "Sat", "Sun"],
                errorbar=None, palette="crest", hue="day", legend=False, ax=ax)
    ax.set(title="Average Tip by Day — Seaborn", xlabel="Day", ylabel="Average tip (USD)")
    saved.append(_save(fig, output_dir / "seaborn_bar_chart.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=tips, x="day", y="total_bill", order=["Thur", "Fri", "Sat", "Sun"],
                color="#8BBF9F", ax=ax)
    ax.set(title="Total Bill by Day — Seaborn", xlabel="Day", ylabel="Total bill (USD)")
    saved.append(_save(fig, output_dir / "seaborn_box_plot.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=tips, x="total_bill", y="tip", hue="smoker", palette="crest", alpha=0.8, ax=ax)
    ax.set(title="Tip vs. Total Bill — Seaborn", xlabel="Total bill (USD)", ylabel="Tip (USD)")
    ax.legend(title="Smoker")
    saved.append(_save(fig, output_dir / "seaborn_scatter_plot.png"))

    corr = tips.select_dtypes(include="number").corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="YlGnBu", vmin=-1, vmax=1, square=True, ax=ax)
    ax.set_title("Numeric Feature Correlations — Seaborn")
    saved.append(_save(fig, output_dir / "seaborn_heatmap.png"))
    return saved


def _save(fig, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def build_all(output_dir: Path = CHARTS_DIR) -> tuple[pd.DataFrame, list[Path]]:
    tips = load_tips()
    files = create_matplotlib_charts(tips, output_dir)
    files.extend(create_seaborn_charts(tips, output_dir))
    return tips, files


if __name__ == "__main__":
    data, charts = build_all()
    print(f"Loaded {len(data)} Tips dataset rows with {len(data.columns)} columns.")
    print(f"Saved {len(charts)} charts to {CHARTS_DIR.resolve()}.")
