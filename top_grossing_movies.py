import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from tabulate import tabulate

def convert_box_office(value):
    if isinstance(value, str):
        value = value.replace('$', '').replace(',', '')
        if 'B' in value:
            return float(value.replace('B', '')) * 1e9
        elif 'M' in value:
            return float(value.replace('M', '')) * 1e6
    return float(value)

def load_data(filepath):
    converters = {'Box Office': convert_box_office}
    return pd.read_csv(filepath, converters=converters)

df = load_data('/home/eyasar/movie_data.csv')

def display_available_movies():
    print("Available Movies:")
    print(tabulate(df[['Title']], headers='keys', tablefmt='psql', showindex=True))

def get_movie_info(title):
    movie = df[df['Title'].str.lower() == title.lower()]
    if movie.empty:
        return "Movie not found."
    else:
        info = movie[['Title', 'Director', 'Cast Members', 'Running Time', 'Awards Won']]
        return tabulate(info, headers='keys', tablefmt='psql')

def plot_top_grossing_movies():
    print("Generating top grossing movies plot...")
    top_movies = df.sort_values(by='Box Office', ascending=False).head(10)
    plt.figure(figsize=(10, 8))
    plt.barh(top_movies['Title'], top_movies['Box Office'], color='skyblue')
    plt.xlabel('Box Office Revenue ($)')
    plt.ylabel('Movie Title')
    plt.title('Top 10 Grossing Movies')
    plt.gca().invert_yaxis()
    plt.savefig('top_grossing_movies.png')  # Save the figure before showing
    plt.show()

def plot_revenue_over_time():
    print("Generating revenue over time plot...")
    data = {'Year': [2010, 2011, 2012, 2013, 2014], 'Revenue': [150, 200, 250, 220, 210]}
    df_time = pd.DataFrame(data)
    fig = px.line(df_time, x='Year', y='Revenue', markers=True,
                  title='Box Office Revenue Over Time',
                  labels={'Revenue': 'Revenue (in millions)'})
    fig.write_image("revenue_over_time.png")  # Save as a static image
    fig.show()

display_available_movies()
movie_title = input("Enter a movie title from the list above: ")
print(get_movie_info(movie_title))

plot_top_grossing_movies()
plot_revenue_over_time()

