"""Content Portfolio Analysis module.

Treats the Netflix content library as an investment portfolio, analysing
how the 'allocation' of content by country and genre has changed over time.
This is an extension not present in the original study (Kanigara, 2021).

Financial analogy:
    - Content categories = asset classes
    - Number of titles = portfolio weight
    - Yearly change = portfolio rebalancing
"""

import pandas as pd
import numpy as np


class ContentPortfolioAnalyser:
    """Analyses Netflix content library as an investment portfolio.

    Computes yearly allocation weights by country and genre, and measures
    diversification using the Herfindahl-Hirschman Index (HHI) — a standard
    concentration metric used in finance and economics.

    Args:
        df (pd.DataFrame): Cleaned DataFrame from NetflixDataCleaner.

    Example:
        >>> analyser = ContentPortfolioAnalyser(clean_df)
        >>> weights = analyser.country_allocation()
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def country_allocation(self, top_n: int = 6) -> pd.DataFrame:
        """Compute yearly content allocation (%) by top contributing countries.

        Financial analogy: asset class weights in a portfolio over time.

        Args:
            top_n (int): Number of top countries to track. Defaults to 6.

        Returns:
            pd.DataFrame: Pivot table with year as index, country as columns,
                values are percentage of total titles that year.
        """
        exploded = self.df.copy()
        exploded["country"] = exploded["country"].str.split(", ")
        exploded = exploded.explode("country").copy()
        exploded["country"] = exploded["country"].str.strip()
        exploded = exploded[exploded["country"] != "Unknown"]

        top_countries = (
            exploded["country"].value_counts().head(top_n).index.tolist()
        )
        exploded = exploded[exploded["country"].isin(top_countries)]

        pivot = (
            exploded.groupby(["year_added", "country"])
            .size()
            .unstack(fill_value=0)
        )
        # Convert to percentage weights
        pivot = pivot.div(pivot.sum(axis=1), axis=0) * 100
        return pivot.dropna()

    def genre_allocation(self, top_n: int = 6) -> pd.DataFrame:
        """Compute yearly content allocation (%) by top genres.

        Args:
            top_n (int): Number of top genres to track. Defaults to 6.

        Returns:
            pd.DataFrame: Pivot table with year as index, genre as columns,
                values are percentage of total titles that year.
        """
        exploded = self.df.copy()
        exploded["genre"] = exploded["listed_in"].str.split(", ")
        exploded = exploded.explode("genre").copy()
        exploded["genre"] = exploded["genre"].str.strip()

        top_genres = (
            exploded["genre"].value_counts().head(top_n).index.tolist()
        )
        exploded = exploded[exploded["genre"].isin(top_genres)]

        pivot = (
            exploded.groupby(["year_added", "genre"])
            .size()
            .unstack(fill_value=0)
        )
        pivot = pivot.div(pivot.sum(axis=1), axis=0) * 100
        return pivot.dropna()

    def herfindahl_index(self) -> pd.DataFrame:
        """Compute the Herfindahl-Hirschman Index (HHI) of content concentration.

        HHI is a standard measure of market/portfolio concentration used in
        finance and economics. Lower HHI = more diversified content library.

        Formula: HHI = sum(market_share_i ^ 2) for all i
        Range: 0 (perfectly diversified) to 10,000 (monopoly)

        Returns:
            pd.DataFrame: DataFrame with 'year_added' and 'hhi' columns.
        """
        exploded = self.df.copy()
        exploded["country"] = exploded["country"].str.split(", ")
        exploded = exploded.explode("country").copy()
        exploded["country"] = exploded["country"].str.strip()
        exploded = exploded[exploded["country"] != "Unknown"]

        yearly = exploded.groupby(["year_added", "country"]).size().reset_index(name="count")
        yearly_total = yearly.groupby("year_added")["count"].transform("sum")
        yearly["share"] = yearly["count"] / yearly_total * 100
        hhi = (
            yearly.groupby("year_added")
            .apply(lambda x: (x["share"] ** 2).sum(), include_groups=False)
            .reset_index(name="hhi")
        )
        return hhi[hhi["year_added"] >= 2015]

    def us_dependency(self) -> pd.DataFrame:
        """Track the share of US content over time as a dependency metric.

        Financial analogy: home bias / concentration risk in a single asset.

        Returns:
            pd.DataFrame: DataFrame with 'year_added' and 'us_share' columns.
        """
        exploded = self.df.copy()
        exploded["country"] = exploded["country"].str.split(", ")
        exploded = exploded.explode("country").copy()
        exploded["country"] = exploded["country"].str.strip()
        exploded = exploded[exploded["country"] != "Unknown"]

        yearly_total = exploded.groupby("year_added").size().reset_index(name="total")
        us_only = (
            exploded[exploded["country"] == "United States"]
            .groupby("year_added")
            .size()
            .reset_index(name="us_count")
        )
        result = yearly_total.merge(us_only, on="year_added", how="left").fillna(0)
        result["us_share"] = result["us_count"] / result["total"] * 100
        return result[result["year_added"] >= 2015]
