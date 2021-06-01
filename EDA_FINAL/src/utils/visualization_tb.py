import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter


class Visualizer:

    def __init__(self, data, expanse, word_stats):
        """ Instance constructor.
            - Args:
                - data: Base Dataframe.
                - expanse: Expanded Dataframe. To expand, use WordCleaner from mining_data_tb.
                - word_stats: Plot word statistics Dataframe. To obtain please use WordClenar from mining_data_tb.
        """
        self.data = data
        self.expanse = expanse
        self.word_stats = word_stats

    def most_common(self, top=5, threshold=30):
        """ Method designed to find the top most popular words of every genre.
            - Args:
                - top: Number of top words to find per genre.
                - threshold: % occurrence to which to obtain the common words.
            - Returns:
                - List of strings.
        """
        tops = []
        for genre in self.word_stats.groupby('genres').count().index:
            tops += list(self.word_stats[self.word_stats.genres == genre].word.head(top).values)
        d = Counter(tops)
        occurrence = {k:(v*100)/len(d) for k, v in d.items()}

        return [k for k, v in occurrence.items() if v > threshold]

    def filter_wordstats(self, top=5, threshold=30, inplace=False):
        """ Function that removes the most common words from the word_stats Dataframe.
            - Args:
                - top: Number of top words to find per genre.
                - threshold: % occurrence to which to obtain the common words.
                - inplace: If True, modifies self.word_stats.
            - Returns:
                - Dataframe
        """
        df = self.word_stats.copy()
        for word in self.most_common(top=top, threshold=threshold):
            df = df[df.word != word]
        if inplace:
            self.word_stats = df
        return df

    def object_to_int(self, x):
        """ Converts years into int values.
        """
        try:
            return int(x)
        except:
            return int(x[:4])

    def decade_df(self, expanse=False):
        """ Returns dataframe with years changed into decades.
        """
        if expanse:
            df = self.expanse.copy()
        else:
            df = self.data.copy()
        df['Year'] = df['Year'].apply(self.object_to_int)
        df.Year = df.Year.round(-1)
        return df

    def plot_year_lineplot(self, y='netflix_rating', genre=None):
        """ Tendency plot over time.
        """
        if genre:
            df = self.decade_df(expanse=True)
            df = df[df.Genre == genre]
            sns.lineplot(data=df, x='Year', y=y, ci=None).set(title=f'{y} evolution over time for {genre}')
        else:
            df = self.decade_df()
            sns.lineplot(data=df, x='Year', y=y, ci=None).set(title=f'{y} evolution over time')

    def plot_displot(self, x='netflix_rating', kde=True, bins='auto', genre=None):
        """ Simple sns.displot function to represent the frequency os a given x-axis from Base Dataframe.
            - Args:
                - x: x-axis
                - kde: present data along with a line graph.
        """
        if genre:
            df = self.expanse[self.expanse.Genre == genre]
            sns.histplot(data=df, x=x, kde=kde, bins=bins).set(title=f'{x} distribution for {genre}')
        else:
            df = self.data.copy()
            sns.histplot(data=df, x=x, kde=kde, bins=bins).set(title=f'{x} distribution')

    def plot_genre_pie(self, top=10):
        """ Pie Chart plot of the Genre distribution of the Expanded Dataframe.
            - Args:
                - top: Top most frequent genres. The remaining categories are grouped under the label 'others'.
        """
        gen = self.expanse.groupby('Genre').count()
        gen_2 = pd.DataFrame(gen['Title']).sort_values('Title', ascending=False)
        others = gen_2.iloc[top:].sum()[0]
        gen_3 = pd.DataFrame(gen_2.iloc[:top-1].unstack())
        gen_3.reset_index(inplace=True)
        gen_3.rename(columns={0:'Total'}, inplace=True)
        gen_3.drop(columns='level_0', inplace=True)
        gen_4 = gen_3.append(pd.DataFrame({'Genre':'Others', 'Total':others}, index=[0]), ignore_index=True)

        pie, ax = plt.subplots(figsize=[10,6])
        labels = gen_4['Genre']
        plt.pie(x=gen_4['Total'], autopct="%.1f%%", labels=labels, pctdistance=0.5)
        plt.title("Titles by Genre", fontsize=14)
        
        plt.show()

    def plot_word_barchart(self, genre, x='%_occurrence', y='word', top=10, sort=0, show_values=False, common=True):
        """ Simple bar chart representing the top words of a given genre ordered by the selected axis.
            - genre: specific genre to plot.
            - x: x-axis
            - y: y-axis
            - top: Top most words.
            - sort: 0 for x-axis and 1 for y-axis.
            - show_labels: Shows value on each bar. Only set to True if the y-axis contains the numeric values.
            - common: If False, filters word_stats by removing the most common word values in all genres. 
        """
        if common == False:
            df = self.filter_wordstats()
        else:
            df = self.word_stats
        if sort == 0:
            data = df[df.genres == genre].sort_values(x, ascending=False).head(top)
        elif sort == 1:
            data = df[df.genres == genre].sort_values(y, ascending=False).head(top)
        x_value = data[x]
        y_value = data[y]
        chart = sns.barplot(x=x_value, y=y_value, color='firebrick')
        chart.set(title=f'Most Popular Words from {genre} Genre')
        if show_values:
            chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
            for p in chart.patches:
                        chart.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')
        plt.show()

    def top_by_genre(self, top=20, common=True):
        """ Method to filter the word_stats Dataframe by the highest % occurrence value.
            - Args:
                - top: top most words for each genre.
                - common: If False, filters word_stats by removing the most common word values in all genres. 
            - Returns:
                - Filtered word_stats Dataframe.
        """
        top = pd.DataFrame(columns=self.word_stats.columns)
        if common == False:
            df = self.filter_wordstats()
        else:
            df = self.word_stats
        for g in list(set(df.genres.values)):
            top = top.append(df[df.genres == g].head(20), ignore_index=True)
        return top

    def plot_treemap(self, top=20, values='%_occurrence', color='mean_rating', width=800, height=400, common=True):
        """ Plots a treemap with the help of the 'top_by_genre' method.
            - Args:
                - top: top most words for each genre.
                - values: numeric value to evaluate.
                - color: numeric value to represent in the color scale.
                - common: If False, filters word_stats by removing the most common word values in all genres. 
        """
        df = self.top_by_genre(top=top, common=common)
        df['Genres'] = 'Genres'
        fig = px.treemap(df.dropna(), path=['Genres','genres','word'], values=values, 
                        color=color, color_continuous_scale='RdBu', title='Word % Occurrence by Genre',
                        width=width, height=height)
        return fig

    def generate_wordcloud(self, genre, values='%_occurrence', common=True, save=False):
        """ Plots a word cloud image of the words of a certain genre.
            - genre: genre to evaluate.
            - values: Determines the word size inside the cloud.
            - common: If False, filters word_stats by removing the most common word values in all genres. 
        """
        if common == False:
            word_stats = self.filter_wordstats()
        else:
            word_stats = self.word_stats
        df = word_stats[word_stats.genres == genre]

        words = df['word'].tolist()
        values = df[values].tolist()
        d = dict(zip(words, values))
        if len(d) > 5:
            text = ''.join([(str(k) + ' ')*round(v) for k, v in d.items()])

            wordcloud = WordCloud(background_color='white', collocations=False).generate(text)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.show()
            if save:
                wordcloud.to_file(f'{genre}_cloud.png')

    def timepie(self):
        categories = {'Data Mining':50, 'Visualization':20, 'Flask':1, 'Streamlit':10, 'SQL': 3, 'Report Analysis':5}
        pie, ax = plt.subplots(figsize=[10,6])
        labels = categories.keys()
        plt.pie(x=categories.values(), autopct="%.1f%%", labels=labels, pctdistance=0.5)
        plt.title("Time spent per Project Step", fontsize=14)

    def heatmap(self, data='base'):
        
        if data == 'expanse':
            df = self.expanse.drop('Unnamed: 0', axis=1)
        elif data == 'word_stats':
            df = self.word_stats.drop(['Unnamed: 0', 'Unnamed: 0.1', 'index'], axis=1)
        else:
            df = self.data.drop('Unnamed: 0', axis=1)

        sns.heatmap(df.corr(), annot=True).set(title=f'{data} Heatmap')