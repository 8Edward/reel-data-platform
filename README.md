# reel-data-platform
Data platform: MovieLens + TMDB -> Postgres -> Airflow -> dbt

## Структура

- `dags/` — DAG Airflow
- `dbt/` — модели dbt
- `src/` — Python-код загрузки данных

## Data sources

- [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) by GroupLens Research, University of Minnesota. Used for non-commercial educational purposes.
- F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. https://doi.org/10.1145/2827872
- [TMDB](https://www.themoviedb.org/): This product uses the TMDB API but is not endorsed or certified by TMDB.
