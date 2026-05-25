"""Core EDA analysis class, reproducing Kanigara (2021) in Python.

Each method corresponds to a section of the original R analysis.
Reproduction differences are documented in method docstrings.
"""

import pandas as pd


class NetflixExplorer:
    """Performs EDA on the cleaned Netflix dataset, reproducing Kanigara (2021).

    Args:
        df (pd.DataFrame): Cleaned DataFrame from NetflixDataCleaner.

    Example:
        >>> explorer = NetflixExplorer(clean_df)
        >>> explorer.content_type_distribution()
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def content_type_distribution(self) -> pd.Series:
        """Count of Movies vs TV Shows (RQ2).

        Reproduction note: matches original R value_counts() exactly.

        Returns:
            pd.Series: Counts indexed by content type.
        """
        return self.df["type"].value_counts()

    def yearly_additions(self) -> pd.DataFrame:
        """Content additions per year grouped by type (RQ1).

        Returns:
            pd.DataFrame: Pivot table with years as index and types as columns.
        """
        return (
            self.df.groupby(["year_added", "type"])
            .size()
            .unstack(fill_value=0)
            .sort_index()
        )

    def top_countries(self, n: int = 10) -> pd.Series:
        """Top N countries by number of titles (RQ3).

        Reproduction note: the original R code uses only the first listed country
        per title. We explode all countries, giving higher counts but same ranking.
        This is documented as an improvement over the original approach.

        Args:
            n (int): Number of top countries to return. Defaults to 10.

        Returns:
            pd.Series: Title counts indexed by country name.
        """
        countries = (
            self.df["country"]
            .str.split(", ")
            .explode()
            .str.strip()
        )
        return countries[countries != "Unknown"].value_counts().head(n)

    def top_genres(self, n: int = 10) -> pd.Series:
        """Top N genres from 'listed_in' column (RQ4).

        Reproduction note: we apply .str.strip() to genre strings; the original
        R code did not, leading to minor count differences due to whitespace.

        Args:
            n (int): Number of top genres to return. Defaults to 10.

        Returns:
            pd.Series: Genre counts indexed by genre name.
        """
        genres = (
            self.df["listed_in"]
            .str.split(", ")
            .explode()
            .str.strip()
        )
        return genres.value_counts().head(n)

    def movie_duration_trend(self) -> pd.DataFrame:
        """Average movie duration per release year (RQ5 — extension).

        This analysis was not present in the original study.

        Returns:
            pd.DataFrame: DataFrame with 'release_year' and 'avg_duration'.
        """
        movies = self.df[self.df["type"] == "Movie"].copy()
        trend = (
            movies.groupby("release_year")["duration_val"]
            .mean()
            .reset_index()
            .rename(columns={"duration_val": "avg_duration"})
        )
        return trend[trend["release_year"] >= 1990]

    def rating_distribution(self) -> pd.Series:
        """Distribution of content ratings (RQ6 — extension).

        This analysis was not present in the original study.

        Returns:
            pd.Series: Counts indexed by rating category.
        """
        return self.df["rating"].value_counts()
