# Movie Rating Prediction

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chrispyles/movie-rating-prediction/master?filepath=notebooks)

In this repository, I attempt to build a linear regression predictor to predict movie ratings based on information about the movie. This is built on 2018 movie data from The Movie Database (TMDb), whose API I queried in making this project.

## Dependencies

The dependencies are listed in the `requirements.txt` file.

## Data

The data from this project is from the TMDb API, which I queried in the [`loading-data.ipynb`](notebooks/loading-data.ipynb) notebook. CSV files of the original and cleaned data are contained in the `data` folder.

## Notebooks

There are a few notebooks in this project, all in the `notebooks` folder. The proper order for looking through them is listed below.

1. `loading-data.ipynb`
2. `data-cleaning-eda.ipynb`
3. `linear-regression-model.ipynb`

By reading the notebooks in this order, you will be able to follow the project. I recommend looking through this project on Binder (link above) because some of the notebooks have IPython widgets that make understanding the thought process far easier.

## Plots

Copies of all plots generated in this project are contained in the `figures` folder.
