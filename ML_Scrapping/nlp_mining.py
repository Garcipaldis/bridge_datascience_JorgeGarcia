import os
import pandas as pd
import numpy as np
import requests
import nltk
from collections import Counter


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

########### VARIABLES #########################################################################################################

genres = ['History', 'Film-Noir', 'Animation', 'War', 'Biography', 'Sport', 'Musical', 
        'Family', 'Western', 'Documentary', 'Music', 'Adventure', 'Romance', 'Drama', 
        'Fantasy', 'Mystery', 'Crime', 'Comedy', 'Short', 'Action', 'Thriller', 'Sci-Fi', 
        'Horror']


########### WORD DATA MINING ##################################################################################################

class WordCleaner:

    def __init__(self, data, expanse=pd.DataFrame(columns={'None':[]}), genre_dfs=None, genre_list=None):
        """ Instance constructor.
            - Args:
                - data: Base Dataframe in which to operate.
                - expanse: Expanded Dataframe by genre.
                - genre_dfs: list of Dataframes by genre.
                - genre_list: genre string list
        """
        self.data = data
        self.expanse = expanse
        if genre_dfs:
            self.genre_dfs = genre_dfs
        else:
            self.genre_dfs = {}
        if genre_list:
            self.genre_list = genre_list
        else:
            self.genre_list = ['History', 'Film-Noir', 'Animation', 'War', 'Biography', 'Sport', 'Musical', 'Family',
        'Western', 'Documentary', 'Music', 'Adventure', 'Romance', 'Drama', 'Fantasy', 'Mystery', 'Crime',
        'Comedy', 'Short', 'Action', 'Thriller', 'Sci-Fi', 'Horror']

    def unfold_by_column_value(self, simple_row, column='Genre'):
        """Function which unfolds a single row by all its column values.
            - Args:
                - simple_row: one single row in the form of Dataframe from which to extract the different values.
                - column: Column to evaluate for the unfolding.
            - Returns:
                - Dataframe with multiple copies of the same row, each one with a unique column value.
        """
        df = pd.DataFrame(columns=simple_row.index)
        row = simple_row.copy()
        for genre in simple_row[column].replace(',', ' ').split():
            row[column] = genre
            df = df.append(row, ignore_index=True)
        return df

    def expand_df(self, column='Genre'):
        """ Function which applies 'unfold_by_column_value' for each row on the Base Dataframe.
            - Args:
                - column: column to evaluate for the unfolding.
                - net_data: Uses the Netflix-IMDb Dataframe by default.
            - Returns:
                - Expanded Dataframe.
        """

        self.data[column] = self.data[column].apply(lambda x: str(x))
        df = pd.DataFrame(columns=self.data.columns)
        for i, row in self.data.iterrows():
            df = df.append(self.unfold_by_column_value(row, column=column))

        df = df[(df.Genre != 'Adult') & (df.Genre != '\\N')]
        self.expanse = df

        return df

    def get_genre_dataframes(self):
        """ Function desgined to insert each Dataframe filtered by the genre values into a list.
            - Returns:
                - List of filtered Dataframes.
        """
        if self.expanse.empty:
            self.expanse = self.expand_df()

        genre_dfs = {g : self.expanse[self.expanse.Genre == g] for g in self.genre_list}

        self.genre_dfs = genre_dfs
        return genre_dfs

    def select_df(self, genre=None):
        """ Function which returns a specific DataFrame. Either Base Dataframe or a filtered one.
            - Args:
                - genre: genre to which to select the Dataframe. 'None' selects the Base Dataframe.
            - Returns:
                - DataFrame.
        """
        if genre == None:
            df = self.data.loc[:, ['netflix_id', 'netflix_rating', 'imdbRating', 'Genre', 'Plot']]
        elif genre != None and self.genre_dfs == {}:
            self.genre_dfs = self.get_genre_dataframes()
            df = self.genre_dfs[genre]
        else:
            df = self.genre_dfs[genre]
        return df

    def get_column_values(self, genre=None, column='Plot'):
        """ Function which extracts the values of a certain column
            - Args:
                - genre: genre from which retrieve a certain filtered Dataframe.
                - column: column from which to extract the values.
            - Returns:
                - list of string values.
        """
        df = self.select_df(genre=genre)

        column_values = [str(row[column]).lower() for i, row in df.iterrows()]
        return column_values

    def get_unique_word_list(self, column_values):
        """ Filters a list of strings by unique values. Also filters with the help nltk library by nouns and adjectives.
            - Args:
                - column_values: list of strings.
            -Returns:
                - filtered list.
        """
        word_list = []
        for item in [str(text).replace(',', '').replace(':', '').replace('.', '').split() for text in column_values]:
            word_list += item
        word_list = list(set(word_list))
        
        tags = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JS']
        tagged = nltk.pos_tag(word_list)
        result = [t[0] for t in tagged if t[1] in tags and len(t[0]) > 1]

        return result

    def search_word_popularity(self, word, genre=None, chosen_rating='netflix_rating'):
        """ Function designed to calculate different stats of a given word on a Dataframe.
        These stats have been specified inside the code to satisfy this EDA Project.
            - Args:
                - word: Word for which to find the stats.
                - genre: Specific genre value to filter.
                - chosen_rating: Title rating to evaluate.
            - Returns:
                - Dataframe containing the specified word stats.
        """
        df = self.select_df(genre=genre)
        dictionary = {'word': word, 'count': 0, 'genres':genre,'title_occurrence':0, '%_occurrence': 0}

        total = len(df)
        column_values = self.get_column_values(genre=genre)
        lista_dics = [Counter(str(column_values[i]).split()) for i in range(len(column_values))]
        
        ratings = []
        for i, d in enumerate(lista_dics):
            if word.lower() in d.keys():
                dictionary['count'] += d[word.lower()]
                dictionary['title_occurrence'] += 1
                if genre == None:
                    gen_list = str(df.loc[i,'Genre']).replace(',', '').split()
                    for gen in gen_list:
                        if gen not in dictionary['genres']:
                            dictionary['genres'] += f'{gen},'
                ratings.append(df.iloc[i][chosen_rating])

        ratings = np.array(ratings)
        ratings = list(ratings[~np.isnan(ratings)])
        dictionary['%_occurrence'] = dictionary['title_occurrence']*100/total
        try:
            dictionary['mean_rating'] = sum(ratings)/len(ratings)
        except ZeroDivisionError:
            dictionary['mean_rating'] = None
        
        return pd.DataFrame(dictionary, index=[0])

    def get_popdf(self, genre=None, threshold=5, chosen_rating='netflix_rating', log=False):
        """ Function applies the 'search_word_popularity' on a loop to a given Dataframe.
        ** ATENTION ** 
        These function has not been optimized and requires a major amount of time and resources to finalize successfully.
        If used, it is recommended to give a short list of words.
            - Args:
                - genre: Specific genre value to filter.
                - threshold: minimum %_occurrence value.
                - chosen_rating: Title rating to evaluate.
                - log: Option to print information about the process during execution.
            - Returns:
                - Dataframe
        """
        column_values = self.get_column_values(genre=genre)
        word_list = self.get_unique_word_list(column_values)

        popdf = pd.DataFrame(columns=['word', 'count', 'genres', 'title_occurrence', '%_occurrence', 'mean_rating'])
        contador = 1
        for word in word_list:
            popdf = popdf.append(self.search_word_popularity(word, genre=genre, chosen_rating=chosen_rating), ignore_index=True)
            if log:
                print(contador, 'rows inserted out of', len(word_list), f'into {genre}_popdf')
            contador += 1
        popdf = popdf.dropna()
        popdf = popdf[popdf['%_occurrence'] > threshold].sort_values('%_occurrence', ascending=False).reset_index()
        return popdf

    def genres_to_popcsv(self, filepath, threshold=5, chosen_rating='netflix_rating'):
        """ Function designed to get the words stats of a given Dataframe filtered by genre up to a certain % of occurrence threshold.
            - Args:
                - threshold: Minimum percentage of occurrence of a given word to be returned in the Dataframe.
                - chosen_rating: Title rating to evaluate.
                - filepath: path where the Dataframes are saved.
            - Returns:
                - None. Instead, the obtained Dataframes are saved as csv files into a given path.
        """
        if self.genre_dfs == {}:
            self.genre_dfs = self.get_genre_dataframes()
            print('Generating list of Dataframes by Genre...')

        for genre in self.genre_list:
            try:
                f = open(f'{filepath}/{genre}_stats.csv')
                f.close()
                print(f'{genre}_stats.csv already exists.')
            except:
                print(f'Generating {genre} Dataframe...')
                popdf = self.get_popdf(genre=genre, threshold=threshold, chosen_rating=chosen_rating, log=True)
                popdf.to_csv(filepath + os.sep + f'{genre}_stats.csv')
                print(f'{genre}_stats.csv successfully saved.')

    def join_genres(self, wordpath):
        """ Simple function designed to join all existing word stats csv files into a single one.
        """
        res_df = pd.DataFrame(columns=['word', 'count', 'genres', 'title_occurrence', '%_occurrence', 'mean_rating'])
        for genre in self.genre_list:
            try:
                f = open(wordpath + os.sep + f'{genre}_stats.csv')
                f.close()
                df = pd.read_csv(wordpath + os.sep + f'{genre}_stats.csv')
                res_df = res_df.append(df)
            except:
                continue
        res_df.to_csv(os.path.dirname(wordpath) + os.sep + 'WORD_STATS.csv')


if __name__ == '__main__':
    from folders_tb import Folders
    rootpath = Folders.add_path(4, jupyter=False)
    key = "7b2c6fff"
    key_2 = 'a855df40'
    omdb = OmdbCleaner(omdb_net_path='data/OMDb General')
    #omdb.join_omdb(f'{rootpath}/EDA Project/data/OMDb General', files=11, save=True)
    omdb.omdb_to_csv(key, f'{rootpath}/EDA_FINAL/data/IMDb_Clean_1.csv', f'{rootpath}/EDA_Scrapping/data/OMDb General',19000)
    omdb.omdb_to_csv(key_2, f'{rootpath}/EDA_FINAL/data/IMDb_Clean_1.csv',f'{rootpath}/EDA_Scrapping/data/OMDb General', 20000)
