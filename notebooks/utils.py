import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

movies = pd.read_csv("../data/cleaned_movie_data.csv")

def plot_vote_avg_dist_by_word(word):
    """
    Plots overlaid histograms of distributions of ratings for synopses that
    do and do not contain `word`
    """
    not_nan_plots = movies.dropna(subset=["overview"])
    idx = not_nan_plots["overview"].str.contains(word)
    
    has_word = not_nan_plots[idx]
    no_word = not_nan_plots[~(idx)]
    
    plt.figure()
    sns.distplot(has_word["vote_average"], label="Present")
    sns.distplot(no_word["vote_average"], label="Not present")
    plt.title("Distribution of Vote Averages, word = '{}'".format(word))
    plt.xlabel("Vote Average")
    plt.legend()
    plt.savefig("../figures/eda-dist-by-word-{}.png".format(word))