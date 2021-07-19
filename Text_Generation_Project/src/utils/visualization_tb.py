import os, sys
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.mining_data_tb import Preprocessor

class Visualizer(Preprocessor):

    def __init__(self, df):
        Preprocessor.__init__(self, df)
        self.text_in_words = []

    def get_word_popularity(self):
        """Returns a dataframe with the most common words from token list."""

        if len(self.text_in_words) == 0:
            self.preprocess(option='word', mode='base')

        tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JS']
        tagged = nltk.pos_tag(self.text_in_words)
        filtered_words = [t[0] for t in tagged if t[1] in tags and len(t[0]) > 1]
        
        dicc = Counter(filtered_words)
        data = {'word':list(dicc.keys()), 'count':list(dicc.values())}

        df = pd.DataFrame(data, index=range(len(data['word'])))

        return df

    def plot_word_barchart(self, x='count', y='word', top=10, sort=0, show_values=False, save=None):
        """ Simple bar chart representing the top words of a given genre ordered by the selected axis.
            - x: x-axis
            - y: y-axis
            - top: Top most words.
            - sort: 0 for x-axis and 1 for y-axis.
            - show_labels: Shows value on each bar. Only set to True if the y-axis contains the numeric values. 
        """

        df = self.get_word_popularity()

        if sort == 0:
            data = df.sort_values(x, ascending=False).head(top)
        elif sort == 1:
            data = df.sort_values(y, ascending=False).head(top)
        x_value = data[x]
        y_value = data[y]
        chart = sns.barplot(x=x_value, y=y_value, color='royalblue')
        chart.set(title=f'Most Popular Words in Quote Collection')
        if show_values:
            chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
            for p in chart.patches:
                        chart.annotate("%.0f" % p.get_height(), (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')
        if save:
            plt.savefig(save + os.sep + f'quote_word_barchart_{sort}.png')
        plt.show()

    def timepie(self, save=None):
        """ Returns pie chart with Project Steps.
        """
        categories = {'Data Mining':5, 'Flask & Streamlit':12, 'SQL': 3, 
                    'Reports and Documentation':7, 'Preproccesing & Modeling':60}
        pie, ax = plt.subplots(figsize=[10,6])
        labels = categories.keys()
        plt.pie(x=categories.values(), autopct="%.1f%%", labels=labels, pctdistance=0.5)
        plt.title("Time spent per Project Step", fontsize=14)
        if save:
            plt.savefig(save + os.sep + "Project_Steps.png")