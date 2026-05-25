"""Module for cleaning and preprocessing the Netflix dataset.

Translates the data cleaning steps from Kanigara (2021) (R/dplyr) to Python/pandas.
Reproduction note: we add .str.strip() on date_added to handle leading whitespace
not handled in the original R code, which caused silent parse failures there.
"""

import pandas as pd


class NetflixDataCleaner:
    """Cleans and preprocesses the raw Netflix DataFrame.

    Args:
        df (pd.DataFrame): Raw Netflix DataFrame from NetflixDataLoader.

    Attributes:
        df (pd.DataFrame): Working copy of the DataFrame.

    Example:
        >>> cleaner = NetflixDataCleaner(raw_df)
        >>> clean_df = cleaner.clean()
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df.copy()

    def drop_duplicates(self) -> "NetflixDataCleaner":
        """Remove duplicate rows based on show_id.

        Returns:
            NetflixDataCleaner: self, for method chaining.
        """
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=["show_id"])
        removed = before - len(self.df)
        if removed:
            print(f"Removed {removed} duplicate rows.")
        return self

    def parse_dates(self) -> "NetflixDataCleaner":
        """Parse 'date_added' to datetime and extract year/month columns.

        Reproduction note: .str.strip() added vs original R code to handle
        leading whitespace found in the CSV, which R's lubridate silently ignored.

        Returns:
            NetflixDataCleaner: self, for method chaining.
        """
        self.df["date_added"] = pd.to_datetime(
            self.df["date_added"].str.strip(), errors="coerce"
        )
        self.df["year_added"] = self.df["date_added"].dt.year
        self.df["month_added"] = self.df["date_added"].dt.month
        return self

    def fill_missing(self) -> "NetflixDataCleaner":
        """Fill or drop key missing values, following Kanigara (2021).

        Returns:
            NetflixDataCleaner: self, for method chaining.
        """
        self.df["country"] = self.df["country"].fillna("Unknown")
        self.df["rating"] = self.df["rating"].fillna("Not Rated")
        self.df["director"] = self.df["director"].fillna("Unknown")
        self.df["cast"] = self.df["cast"].fillna("Unknown")
        self.df = self.df.dropna(subset=["date_added", "duration"])
        return self

    def parse_duration(self) -> "NetflixDataCleaner":
        """Extract numeric duration for Movies (minutes) and TV Shows (seasons).

        Returns:
            NetflixDataCleaner: self, for method chaining.
        """
        movies = self.df["type"] == "Movie"
        self.df.loc[movies, "duration_val"] = (
            self.df.loc[movies, "duration"]
            .str.replace(" min", "", regex=False)
            .astype(float)
        )
        tv = self.df["type"] == "TV Show"
        self.df.loc[tv, "duration_val"] = (
            self.df.loc[tv, "duration"]
            .str.replace(" Season", "", regex=False)
            .str.replace("s", "", regex=False)
            .astype(float)
        )
        return self

    def clean(self) -> pd.DataFrame:
        """Run the full cleaning pipeline.

        Returns:
            pd.DataFrame: Cleaned DataFrame ready for analysis.
        """
        return (
            self.drop_duplicates()
            .parse_dates()
            .fill_missing()
            .parse_duration()
            .df
        )
