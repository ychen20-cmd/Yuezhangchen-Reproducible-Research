"""Main entry point for the Netflix EDA reproduction + extension pipeline."""

import argparse
from pathlib import Path

from netflix_analysis.data import NetflixDataLoader, NetflixDataCleaner
from netflix_analysis.analysis import NetflixExplorer, ContentPortfolioAnalyser, ContentGrowthForecaster
from netflix_analysis.visualization import NetflixPlotter


def parse_args():
    parser = argparse.ArgumentParser(description="Netflix EDA Reproduction Pipeline")
    parser.add_argument("--data", type=Path, default=Path("data/netflix_titles.csv"))
    parser.add_argument("--output", type=Path, default=Path("output/figures"))
    return parser.parse_args()


def run_pipeline(data_path, output_dir):
    print("=" * 55)
    print("Netflix EDA — Reproduction of Kanigara (2021)")
    print("=" * 55)

    # 1. Load & clean
    print("\n[1/5] Loading data...")
    loader = NetflixDataLoader(data_path)
    raw_df = loader.load()

    print("\n[2/5] Cleaning data...")
    clean_df = NetflixDataCleaner(raw_df).clean()
    print(f"Clean dataset: {len(clean_df):,} rows")

    plotter = NetflixPlotter(output_dir)

    # 3. Original reproduction analyses (RQ1-RQ6)
    print("\n[3/5] Reproducing original analyses (RQ1-RQ6)...")
    explorer = NetflixExplorer(clean_df)
    plotter.plot_type_distribution(explorer.content_type_distribution())
    plotter.plot_yearly_additions(explorer.yearly_additions())
    plotter.plot_top_countries(explorer.top_countries())
    plotter.plot_top_genres(explorer.top_genres())
    plotter.plot_movie_duration_trend(explorer.movie_duration_trend())
    plotter.plot_rating_distribution(explorer.rating_distribution())

    # 4. Portfolio analysis extension (Direction 1)
    print("\n[4/5] Running portfolio analysis extension...")
    portfolio = ContentPortfolioAnalyser(clean_df)
    plotter.plot_country_allocation(portfolio.country_allocation())
    plotter.plot_genre_allocation(portfolio.genre_allocation())
    plotter.plot_hhi(portfolio.herfindahl_index())
    plotter.plot_us_dependency(portfolio.us_dependency())

    # 5. Growth forecasting extension (Direction 3)
    print("\n[5/5] Running growth forecasting extension...")
    forecaster = ContentGrowthForecaster(clean_df)
    plotter.plot_growth_forecast(
        forecaster.linear_forecast(forecast_years=3),
        forecaster.r_squared()
    )
    plotter.plot_moving_average(forecaster.moving_average())
    plotter.plot_yoy_growth(forecaster.growth_rate())

    print(f"\nDone! All {13} figures saved to: {output_dir}")


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.data, args.output)
