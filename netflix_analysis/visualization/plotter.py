"""Visualization class for Netflix EDA using matplotlib and seaborn."""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import seaborn as sns

NETFLIX_RED = "#E50914"


class NetflixPlotter:
    """Generates and saves all visualizations for the Netflix analysis.

    Args:
        output_dir (str | Path): Directory where figures will be saved.
    """

    def __init__(self, output_dir="output/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        sns.set_theme(style="darkgrid")

    def _save(self, filename):
        path = self.output_dir / filename
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"Saved: {path}")

    # Original reproduction plots
    def plot_type_distribution(self, series):
        """Bar chart of Movies vs TV Shows."""
        fig, ax = plt.subplots(figsize=(7, 5))
        series.plot(kind="bar", ax=ax, color=[NETFLIX_RED, "#221F1F"], edgecolor="white")
        ax.set_title("Movies vs TV Shows on Netflix", fontsize=14, fontweight="bold")
        ax.set_xlabel("Content Type"); ax.set_ylabel("Number of Titles")
        ax.tick_params(axis="x", rotation=0)
        self._save("type_distribution.png")

    def plot_yearly_additions(self, pivot):
        """Stacked area chart of yearly content additions."""
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind="area", ax=ax, color=[NETFLIX_RED, "#221F1F"], alpha=0.8)
        ax.set_title("Content Added to Netflix per Year", fontsize=14, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("Number of Titles Added")
        self._save("yearly_additions.png")

    def plot_top_countries(self, series):
        """Horizontal bar chart of top contributing countries."""
        fig, ax = plt.subplots(figsize=(9, 6))
        series.sort_values().plot(kind="barh", ax=ax, color=NETFLIX_RED)
        ax.set_title("Top 10 Countries by Number of Titles", fontsize=14, fontweight="bold")
        ax.set_xlabel("Number of Titles")
        self._save("top_countries.png")

    def plot_top_genres(self, series):
        """Horizontal bar chart of top genres."""
        fig, ax = plt.subplots(figsize=(9, 6))
        series.sort_values().plot(kind="barh", ax=ax, color="#564d4d")
        ax.set_title("Top 10 Genres on Netflix", fontsize=14, fontweight="bold")
        ax.set_xlabel("Number of Titles")
        self._save("top_genres.png")

    def plot_movie_duration_trend(self, df):
        """Line chart of average movie duration over the years."""
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df["release_year"], df["avg_duration"], color=NETFLIX_RED, linewidth=2)
        ax.fill_between(df["release_year"], df["avg_duration"], alpha=0.15, color=NETFLIX_RED)
        ax.set_title("Average Movie Duration Over Time", fontsize=14, fontweight="bold")
        ax.set_xlabel("Release Year"); ax.set_ylabel("Average Duration (minutes)")
        self._save("movie_duration_trend.png")

    def plot_rating_distribution(self, series):
        """Pie chart of content rating distribution."""
        fig, ax = plt.subplots(figsize=(8, 8))
        series.head(8).plot(kind="pie", ax=ax, autopct="%1.1f%%",
            colors=sns.color_palette("Reds_r", len(series)), startangle=90)
        ax.set_ylabel("")
        ax.set_title("Content Rating Distribution", fontsize=14, fontweight="bold")
        self._save("rating_distribution.png")

    # Portfolio analysis plots
    def plot_country_allocation(self, pivot):
        """Stacked area chart: content allocation by country (portfolio weights)."""
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind="area", ax=ax, colormap="Set2", alpha=0.85, stacked=True)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title("Netflix Content Allocation by Country Over Time\n(Portfolio analogy: asset class weights)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("Share of Total Content (%)")
        ax.legend(loc="upper left", fontsize=9)
        self._save("portfolio_country_allocation.png")

    def plot_genre_allocation(self, pivot):
        """Stacked area chart: content allocation by genre."""
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind="area", ax=ax, colormap="tab10", alpha=0.8, stacked=True)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title("Netflix Content Allocation by Genre Over Time", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("Share of Total Content (%)")
        ax.legend(loc="upper left", fontsize=9)
        self._save("portfolio_genre_allocation.png")

    def plot_hhi(self, hhi_df):
        """Line chart: HHI concentration index over time."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hhi_df["year_added"], hhi_df["hhi"], color=NETFLIX_RED, linewidth=2.5, marker="o", markersize=6)
        ax.fill_between(hhi_df["year_added"], hhi_df["hhi"], alpha=0.1, color=NETFLIX_RED)
        ax.set_title("Content Concentration: Herfindahl-Hirschman Index (HHI)\nLower HHI = More Diversified Content Library", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("HHI Score")
        self._save("portfolio_hhi.png")

    def plot_us_dependency(self, dep_df):
        """Line chart: US content share over time (concentration risk)."""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dep_df["year_added"], dep_df["us_share"], color="#221F1F", linewidth=2.5, marker="o", markersize=6)
        ax.fill_between(dep_df["year_added"], dep_df["us_share"], alpha=0.1, color="#221F1F")
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title("US Content Share Over Time\n(Portfolio analogy: home bias / concentration risk)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("US Content Share (%)")
        self._save("portfolio_us_dependency.png")

    # Forecasting plots
    def plot_growth_forecast(self, forecast_df, r2):
        """Bar + line chart: historical additions with OLS forecast."""
        fig, ax = plt.subplots(figsize=(12, 6))
        hist = forecast_df[~forecast_df["is_forecast"]]
        fut = forecast_df[forecast_df["is_forecast"]]
        ax.bar(hist["year_added"], hist["count"], color=NETFLIX_RED, alpha=0.6, label="Actual additions", zorder=2)
        ax.plot(forecast_df["year_added"], forecast_df["forecast"], color="#221F1F", linewidth=2.5, linestyle="--", label=f"OLS trend (R²={r2:.2f})", zorder=3)
        ax.bar(fut["year_added"], fut["forecast"], color="#b3b3b3", alpha=0.7, label="Forecast", zorder=2)
        ax.axvline(x=2021.5, color="gray", linestyle=":", linewidth=1.5)
        ax.text(2021.7, ax.get_ylim()[1] * 0.9, "Forecast →", fontsize=9, color="gray")
        ax.set_title("Netflix Content Growth: Historical Trend & OLS Forecast\n(Financial analogy: trend projection model)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("Number of Titles Added")
        ax.legend()
        self._save("forecast_growth.png")

    def plot_moving_average(self, ma_df):
        """Bar + line chart: content additions with moving average overlay."""
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.bar(ma_df["year_added"], ma_df["count"], color=NETFLIX_RED, alpha=0.5, label="Actual additions")
        ax.plot(ma_df["year_added"], ma_df["ma"], color="#221F1F", linewidth=2.5, marker="o", label="3-Year Moving Average")
        ax.set_title("Content Additions with 3-Year Moving Average\n(Financial analogy: MA technical indicator)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("Number of Titles Added")
        ax.legend()
        self._save("forecast_moving_average.png")

    def plot_yoy_growth(self, growth_df):
        """Bar chart: year-over-year growth rate."""
        fig, ax = plt.subplots(figsize=(10, 5))
        colors = [NETFLIX_RED if v >= 0 else "#221F1F" for v in growth_df["yoy_growth_pct"]]
        ax.bar(growth_df["year_added"], growth_df["yoy_growth_pct"], color=colors)
        ax.axhline(y=0, color="black", linewidth=0.8)
        ax.yaxis.set_major_formatter(mtick.PercentFormatter())
        ax.set_title("YoY Growth Rate of Netflix Content Additions\n(Financial analogy: annual return)", fontsize=13, fontweight="bold")
        ax.set_xlabel("Year"); ax.set_ylabel("YoY Growth (%)")
        self._save("forecast_yoy_growth.png")
