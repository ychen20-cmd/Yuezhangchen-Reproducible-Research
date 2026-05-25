"""Module for loading the Netflix dataset.

Reproduces the data loading step from Kanigara (2021), originally written in R.
Original source: https://github.com/evankanigara/Netflix-Movies-and-TV-Show-EDA
"""

import pandas as pd
from pathlib import Path


class NetflixDataLoader:
    """Handles loading of the Netflix Movies and TV Shows dataset.

    Args:
        data_path (str | Path): Path to the CSV data file.

    Attributes:
        data_path (Path): Resolved path to the dataset.
        raw_df (pd.DataFrame | None): Raw loaded DataFrame, or None before loading.

    Example:
        >>> loader = NetflixDataLoader("data/netflix_titles.csv")
        >>> df = loader.load()
    """

    def __init__(self, data_path: str | Path) -> None:
        self.data_path = Path(data_path)
        self.raw_df: pd.DataFrame | None = None

    def load(self) -> pd.DataFrame:
        """Load the dataset from the CSV file.

        Returns:
            pd.DataFrame: Raw Netflix dataset.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at: {self.data_path}")
        self.raw_df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.raw_df):,} records from {self.data_path.name}")
        return self.raw_df

    def get_info(self) -> dict:
        """Return basic metadata about the loaded dataset.

        Returns:
            dict: Dictionary with keys 'rows', 'columns', 'missing_values'.

        Raises:
            RuntimeError: If data has not been loaded yet.
        """
        if self.raw_df is None:
            raise RuntimeError("Data not loaded. Call .load() first.")
        return {
            "rows": len(self.raw_df),
            "columns": list(self.raw_df.columns),
            "missing_values": self.raw_df.isnull().sum().to_dict(),
        }
