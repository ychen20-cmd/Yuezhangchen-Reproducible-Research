"""Growth Trend Forecasting module.

Forecasts Netflix content additions using linear regression and moving averages,
drawing parallels to trend analysis and forecasting models used in finance.
This is an extension not present in the original study (Kanigara, 2021).

Financial analogy:
    - Yearly content additions = time series of asset volumes
    - Linear regression = trend line (like a simple price trend model)
    - Moving average = smoothed signal (like MA indicators in technical analysis)
"""

import numpy as np
import pandas as pd


class ContentGrowthForecaster:
    """Forecasts Netflix content growth using regression and moving averages.

    Args:
        df (pd.DataFrame): Cleaned DataFrame from NetflixDataCleaner.

    Example:
        >>> forecaster = ContentGrowthForecaster(clean_df)
        >>> forecast = forecaster.linear_forecast(forecast_years=3)
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self._yearly: pd.DataFrame | None = None

    def _get_yearly_counts(self) -> pd.DataFrame:
        """Compute total yearly content additions.

        Returns:
            pd.DataFrame: DataFrame with 'year_added' and 'count' columns.
        """
        if self._yearly is None:
            self._yearly = (
                self.df.groupby("year_added")
                .size()
                .reset_index(name="count")
            )
            self._yearly = self._yearly[
                (self._yearly["year_added"] >= 2015)
                & (self._yearly["year_added"] <= 2021)
            ]
        return self._yearly

    def moving_average(self, window: int = 3) -> pd.DataFrame:
        """Compute a simple moving average of yearly content additions.

        Financial analogy: MA indicators used in technical analysis to smooth
        out short-term fluctuations and identify long-term trends.

        Args:
            window (int): Rolling window size in years. Defaults to 3.

        Returns:
            pd.DataFrame: DataFrame with 'year_added', 'count', and 'ma' columns.
        """
        yearly = self._get_yearly_counts().copy()
        yearly["ma"] = yearly["count"].rolling(window=window, min_periods=1).mean()
        return yearly

    def linear_forecast(self, forecast_years: int = 3) -> pd.DataFrame:
        """Forecast content additions using Ordinary Least Squares (OLS) regression.

        Financial analogy: linear trend models used in financial forecasting
        to project future values based on historical growth patterns.

        Args:
            forecast_years (int): Number of years to forecast beyond 2021.

        Returns:
            pd.DataFrame: DataFrame with historical data and forecast,
                columns: 'year_added', 'count', 'fitted', 'forecast', 'is_forecast'.
        """
        yearly = self._get_yearly_counts().copy()

        x = yearly["year_added"].values
        y = yearly["count"].values

        # OLS: fit y = a + b*x
        x_mean, y_mean = x.mean(), y.mean()
        b = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        a = y_mean - b * x_mean

        yearly["fitted"] = a + b * yearly["year_added"]
        yearly["is_forecast"] = False

        # Future years
        future_years = list(range(int(x.max()) + 1, int(x.max()) + forecast_years + 1))
        future_df = pd.DataFrame({
            "year_added": future_years,
            "count": np.nan,
            "fitted": np.nan,
            "is_forecast": True,
        })
        future_df["forecast"] = a + b * future_df["year_added"]

        result = pd.concat([yearly, future_df], ignore_index=True)
        result["forecast"] = result["forecast"].combine_first(result["fitted"])
        return result

    def r_squared(self) -> float:
        """Compute R-squared of the linear regression fit.

        Financial analogy: goodness-of-fit measure used to assess how well
        a trend model explains historical variation.

        Returns:
            float: R-squared value between 0 and 1.
        """
        yearly = self._get_yearly_counts()
        x = yearly["year_added"].values
        y = yearly["count"].values
        x_mean, y_mean = x.mean(), y.mean()
        b = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
        a = y_mean - b * x_mean
        y_pred = a + b * x
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        return float(1 - ss_res / ss_tot)

    def growth_rate(self) -> pd.DataFrame:
        """Compute year-over-year growth rate of content additions.

        Financial analogy: YoY return calculation used in performance analysis.

        Returns:
            pd.DataFrame: DataFrame with 'year_added', 'count', 'yoy_growth_pct'.
        """
        yearly = self._get_yearly_counts().copy()
        yearly["yoy_growth_pct"] = yearly["count"].pct_change() * 100
        return yearly.dropna()
