"""Analysis subpackage for Netflix EDA."""

from netflix_analysis.analysis.explorer import NetflixExplorer
from netflix_analysis.analysis.portfolio import ContentPortfolioAnalyser
from netflix_analysis.analysis.forecaster import ContentGrowthForecaster

__all__ = ["NetflixExplorer", "ContentPortfolioAnalyser", "ContentGrowthForecaster"]
