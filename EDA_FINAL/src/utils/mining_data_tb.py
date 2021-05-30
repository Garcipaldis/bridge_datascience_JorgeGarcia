
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

net_path = 'data/Netflix_raw/movie_titles.csv'
imdb_path = 'data/IMDb Datasets/types.tsv'
omdb_net_path = 'data/OMDb Netflix'

########### OMDB DATA MINING ##################################################################################################

class OmdbCleaner:

    def __init__(self, net_path='data/Netflix_raw/movie_titles.csv', 
                imdb_path='data/IMDb Datasets/types.tsv', omdb_net_path='data/OMDb Netflix'):
        self.net_path = net_path
        self.imdb_path = imdb_path
        self.omdb_net_path = omdb_net_path

    def float_to_object(self, x):
        """Transform a float into a string without decimals. Else returns variable.
        """
        try:
            return str(int(x))
        except ValueError:
            return x

    def get_imdb_ids(self, save=False):
        """ Function which finds the IMDb ID of the titles from the Netflix Movie Data.
            - Args:
                - save: Option of saving DataFrame into a .csv file.
            - Returns:
                - Dataframe.
        """
        net_movies = pd.read_csv(self.net_path, names=['netflix_id', 'startYear', 'originalTitle'])
        net_movies['startYear'] = net_movies['startYear'].apply(self.float_to_object)

        imdb_df = pd.read_csv(self.imdb_path, sep='\t', low_memory=False)

        net_data = pd.merge(net_movies, imdb_df, on=['originalTitle', 'startYear'])
        net_data.rename(columns={'tconst':'titleId'}, inplace=True)
        net_data.drop_duplicates('originalTitle', inplace=True)
        if save == True:
            net_data.to_csv(f'{self.net_path}/Net_Data_ID.csv')

        return net_data

    def omdb_to_csv(self, filepath, row_start, row_num=999, key='7b2c6fff'):
        """Function design to obtain dataframes by calling the OMDb API. Said API is returns IMDb stats for a certain title.
            - Args:
                - filepath: .csv filepath containing the IMDb IDs of the desired titles (ej.'Net_Data_ID.csv').
                - row_start: row from which to start sending API requests.
                - row_num: Number of rows starting from row_start from which the API request is done.
                - key: API key necessary in order to access the data. Obtained via: "http://www.omdbapi.com/apikey.aspx"
            -Returns:
                - Dataframe
        """
        movies = pd.read_csv(filepath)
        data = []
        count = 1

        for titleid in movies.loc[row_start:(row_start+row_num), 'titleId']:
            omdb_url = f'http://www.omdbapi.com/?i={titleid}&apikey={key}'
            r = requests.get(omdb_url, params={'plot':'full'}).json()
            data.append(r)
            print(count, 'Response:', r['Response'])
            count += 1

        df = pd.DataFrame(data)
        df.to_csv(f'Data_OMDb_{row_start}.csv')
        return df

    def join_omdb(self, omdb_net_path, files=10, save=False):
        """ Function design to merge existing OMDb csv files.
            - Args:
                - omdb_net_path: where the csv files are located.
                - files: number of files to read.
                - save: Option of saving DataFrame into a .csv file.
            - Returns:
                - Dataframe.
        """
        data = []
        for i in range(files):
            if i > 0:
                data.append(pd.read_csv(f'{omdb_net_path}/Data_OMDb_{i}000.csv'))
            else:
                data.append(pd.read_csv(f'{omdb_net_path}/Data_OMDb_{i}.csv'))
        df = pd.concat(data)
        df = df.drop_duplicates().dropna(how='all').drop('Unnamed: 0', axis=1)

        cleaned = df.sort_values('imdbRating', ascending=False).loc[:,['imdbID', 'Title', 'Year', 'imdbRating','Genre', 'Plot']]
        cleaned = cleaned.dropna(how='any').reset_index().loc[:,'imdbID':]

        if save == True:
            cleaned.to_csv(f'{omdb_net_path}/OMDb_Net_Data.csv')

        return cleaned

########### NETFLIX DATA MINING #################################################################################################

class NetCleaner:

    def combined_to_list(self, path):
        """ Function which transforms Netflix's 'Combined.text' files for later operations.
            - Args:
                - path: filepath where 'combined_data_x.txt' is located.
            -Returns:
                - List of dictionaries
        """
        with open(path, 'r') as raw:
            text = raw.readlines()
        res = []
        k = []
        for line in text:
            if ':' not in line:
                res.append(k + line.strip('\n').split(','))
            else:
                k = [line.strip(':\n')]
        return res

    def combined_to_csv(self, path, num=0, save=False):
        """ Function designed to transform Netflix's 'combined.txt' file into a DataFrame. It uses the 'combined_to_list' function.
            - Args:
                - path: filapath where 'combined_data_x.txt' is located.
                - num: combined file number (ej. 'combined_data_1.txt').
                - save: Option of saving DataFrame into a .csv file.
            - Returns:
                - Dataframe.
        """
        lista = self.combined_to_list(path)
        df = pd.DataFrame(lista, columns=['netflix_id', 'user_id', 'rating', 'date'])
        if save == True:
            df.to_csv(f'data/Net_combined_{num}.csv')
        return df

    def get_title_ratings(self, folder_path, net_path, save=False):
        """ Function which get all the transformed Netflix's 'combined.txt' data, 
        groups it by title and merges it with Net Movie Data.
            - Args:
                - folderpath: folder containing the 'Net_combined' data.
                - net_path: filepath of the netflix movie list.
                - save: Option of saving DataFrame into a .csv file.
            - Returns:
                - Dataframe.
        """

        c1 = pd.read_csv(f'{folder_path}/Net_combined_1.csv')
        c2 = pd.read_csv(f'{folder_path}/Net_combined_2.csv')
        c3 = pd.read_csv(f'{folder_path}/Net_combined_3.csv')
        c4 = pd.read_csv(f'{folder_path}/Net_combined_4.csv')

        c = [c1, c2, c3, c4]
        net_comb_data = pd.concat(c)
        
        net_comb_data.rating = net_comb_data.rating.apply(lambda x: x*2)
        titles = net_comb_data.groupby('netflix_id').agg({'rating':'mean', 'user_id': 'count'})
        titles = titles.rename(columns={'rating':'netflix_rating', 'Number of votes':'number_of_votes'})
        net_movies = pd.read_csv(net_path, names=['netflix_id', 'startYear', 'Title'])
        df = pd.merge(titles, net_movies.loc[:, ['netflix_id', 'Title']], on='netflix_id')
        
        if save == True:
            net_comb_data.to_csv('data/Netflix_Comb_Data.csv')
            df.to_csv('data/Net_title_ratings.csv')
        
        return df

    def get_base_dataframe(self, net_ratings_path, omdb_net_path, save=False):
        """ Function designed to merge netflix ratings vs omdb data in order to obtain a base dataframe
        from which to make future transformations.
            - Args:
                - net_ratings_path: path containing the net ratings csv.
                - omdb_net_path: path containing the omdb data csv.
                - save: Option of saving DataFrame into a .csv file.
            - Returns:
                - Base Dataframe
        """
        net_ratings = pd.read_csv(net_ratings_path)
        omdb_net_data = pd.read_csv(omdb_net_path)
        base_df = pd.merge(net_ratings, omdb_net_data, on='Title')
        base_df = base_df.drop('Unnamed: 0_x', axis=1).drop('Unnamed: 0_y', axis=1).drop_duplicates('netflix_id')
        base_df = base_df.loc[:, 'netflix_id':'Type']
        if save == True:
            base_df.to_csv('BASE_DATASET.csv')
        
        return base_df

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
        'Comedy', 'Short', 'Action', 'Thriller', 'Sci-Fi', 'Horror', 'Adult']

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
        for genre in simple_row[column].replace(',', '').split():
            row[column] = genre
            df = df.append(row, ignore_index=True)
        return df

    def expand_df(self, column='Genre', net_data=True):
        """ Function which applies 'unfold_by_column_value' for each row on the Base Dataframe.
            - Args:
                - column: olumn to evaluate for the unfolding.
                - net_data: Uses the Netflix-IMDb Dataframe by default.
            - Returns:
                - Expanded Dataframe.
        """
        self.data[column] = self.data[column].apply(lambda x: str(x))
        df = pd.DataFrame(columns=self.data.columns)
        if net_data:
            filtered_data = self.data.loc[:, ['netflix_id', 'netflix_rating', 'imdbRating', 'Genre', 'Plot']]
        elif net_data == False:
            filtered_data = self.data.loc[:, ['imdbID', 'imdbRating','Genre', 'Plot']]
        for i, row in filtered_data.iterrows():
            df = df.append(self.unfold_by_column_value(row, column=column))

        self.expanse = df
        return df

    def get_genre_dataframes(self):
        """ Function desgined to insert each Dataframe filtered by the genre values into a list.
            - Returns:
                - List of filtered Dataframes.
        """
        if self.expanse.empty:
            self.expanse = self.expand_df(self.data)

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

    def genres_to_popcsv(self, threshold=5, chosen_rating='netflix_rating', filepath='data/Word_Stats'):
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
            except:
                print(f'Generating {genre} Dataframe...')
                popdf = self.get_popdf(genre=genre, threshold=threshold, chosen_rating=chosen_rating, log=True)
                popdf.to_csv(f'{filepath}/{genre}_stats.csv')
                print(f'{genre}_stats.csv successfully saved.')

    def join_genres(self):
        """ Simple function designed to join all existing word stats csv files into a single one.
        """
        res_df = pd.DataFrame(columns=['word', 'count', 'genres', 'title_occurrence', '%_occurrence', 'mean_rating'])
        for genre in self.genre_list:
            try:
                f = open(f'data/Word_Stats/{genre}_stats.csv')
                f.close()
                df = pd.read_csv(f'data/Word_Stats/{genre}_stats.csv')
                res_df = res_df.append(df)
            except:
                continue
        res_df.to_csv('data/WORD_STATS.csv')


if __name__ == '__main__':
    from folders_tb import add_path
    rootpath = add_path(4, jupyter=False)
    key_2 = 'a855df40'
    omdb = OmdbCleaner(omdb_net_path='data/OMDb General')
    omdb.join_omdb(f'{rootpath}/EDA Project/data/OMDb General', files=11, save=True)
    #omdb.omdb_to_csv(f'{rootpath}/EDA Project/data/IMDb_Clean_1.csv', 9000)
    #omdb.omdb_to_csv(f'{rootpath}/EDA Project/data/IMDb_Clean_1.csv', 10000, key=key_2)
    """rootpath = add_path(4, jupyter=False)
    data = pd.read_csv(f'{rootpath}/EDA Project/MAIN_DATASET.csv')
    expanse = pd.read_csv(f'{rootpath}/EDA Project/GENRE_DATASET.csv')
    wcleaner = word_cleaner(data, expanse=expanse)
    print(wcleaner.get_popdf(genre='War', log=True))"""
