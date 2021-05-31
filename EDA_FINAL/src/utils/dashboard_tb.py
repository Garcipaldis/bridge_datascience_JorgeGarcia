import streamlit as st
import pandas as pd
from PIL import Image
import os, sys
import requests

sys.path.append(os.path.dirname(__file__))

from utils.visualization_tb import Visualizer

class StreamFuncs:

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
        self.viz = Visualizer(data, expanse, word_stats)

    def greet(self):
        st.subheader('EDA made by: Jorge García Navarro')
        st.write("\nThe purpose of this study is to find the most common words under each Netflix Title Plot grouped by Genre.")
        st.write("Furthermore, these popular words will be compared to the user ratings in order to find a possible correlation.""")
        st.subheader('Hypothesis')
        st.write("'The genre Drama has the highest mean rating and its most popular words are: murder and vengeance.'")
        st.pyplot(self.viz.generate_wordcloud('Romance', common=False))
        st.write('Romance Word Cloud')
        st.subheader('Plot Example')
        st.write("""Following a truck hijack in New York, five conmen are arrested and brought together for questioning. 
                As none of them are guilty, they plan a revenge operation against the police. 
                The operation goes well, but then the influence of a legendary mastermind criminal called Keyser Söze is felt. 
                It becomes clear that each one of them has wronged Söze at some point and must pay back now. 
                The payback job leaves 27 men dead in a boat explosion, but the real question arises now: Who actually is Keyser Söze?""")
        st.write('Title: The Usual Suspects')
        st.write('Genres: Crime, Mystery, Thriller')

    def piechart_page(self):
        top = st.sidebar.select_slider("Top Values",
                                    options=range(3, 21),
                                    value=10)
        st.pyplot(self.viz.plot_genre_pie(top))
    
    def distribution_page(self):
        droplist = st.sidebar.selectbox('Select Column Value:',
                            options=['netflix_rating', 'imdbRating','Metascore'])
        kde = st.sidebar.checkbox('kde')
        genre = st.sidebar.selectbox('Select Genre:',
                            options=['All'] + list(self.expanse.groupby('Genre').count().index))
        if genre == 'All':
            st.pyplot(self.viz.plot_displot(x=droplist, kde=kde))
        else:
            st.pyplot(self.viz.plot_displot(x=droplist, kde=kde, genre=genre))

    def tendency_page(self):
        droplist = st.sidebar.selectbox('Select Column Value:',
                                options=['netflix_rating', 'imdbRating', 'Metascore'])
        genre = st.sidebar.selectbox('Select Genre:',
                                options=['All'] + list(self.expanse.groupby('Genre').count().index))
        if genre == 'All':
            st.pyplot(self.viz.plot_year_lineplot(y=droplist))
        else:
            st.pyplot(self.viz.plot_year_lineplot(y=droplist, genre=genre))

    def cloud_page(self, path):
        cloudpath = os.path.dirname(path) + os.sep + 'resources' + os.sep + 'wordclouds'
        for f in os.listdir(cloudpath):
            image = Image.open(cloudpath + os.sep + f)
            st.subheader(f.split('_')[0])
            st.image(image)

    def treemap_page(self):
        common = st.sidebar.checkbox('Use common words', value=True)
        st.plotly_chart(self.viz.plot_treemap(width=1000, height=600, common=common))

    def barchart_page(self):
        droplist = st.sidebar.selectbox('Select Genre:',
                                options=list(self.expanse.groupby('Genre').count().index))
        top = st.sidebar.select_slider("Top Values",
                                        options=range(3, 21),
                                        value=10)
        common = st.sidebar.checkbox('Use common words', value=True)
        vertical = st.sidebar.checkbox('Vertical')
        if vertical:
            st.pyplot(self.viz.plot_word_barchart(droplist, x='word', y='%_occurrence',top=top, sort=1, show_values=True, common=common))
        else:
            st.pyplot(self.viz.plot_word_barchart(droplist, top=top, common=common))

    def flask_page(self):
        r = requests.get(url="http://localhost:6060/info?token_id=B53814652")
        response = r.json()
        df = pd.DataFrame(response).dropna()
        df = df.iloc[:, [4, 2, 5, 20, 9, 13]]
        
        droplist = st.sidebar.selectbox('Order by:',
                                options=['Netflix User Rating', 'IMDBb Rating', 'Year'])
        ascending = st.sidebar.checkbox('Ascending')
        if droplist == 'Netflix User Rating':
            if ascending:
                df.sort_values('netflix_rating', inplace=True)
            else:
                df.sort_values('netflix_rating', inplace=True, ascending=False)
        elif droplist == 'IMDBb Rating':
            if ascending:
                df.sort_values('imdbRating', inplace=True)
            else:
                df.sort_values('imdbRating', inplace=True, ascending=False)
        elif droplist == 'Year':
            if ascending:
                df.sort_values('Year', inplace=True)
            else:
                df.sort_values('Year', inplace=True, ascending=False)
        st.dataframe(df)

    def conclude(self):
        st.subheader('1. Was it possible to demonstrate the hypothesis? Why?')
        st.write("""After many data transformations on the Base Dataset, it was possible to find an answer to the stated hypothesis. 
                The analyzed data showed not only that the best rated genre was Film-Noir instead of Drama, 
                but neither 'murder' nor 'vengeance' were in the top 20.""")
        st.subheader('2. What can you conclude about your data study?')
        st.write("""Based on the analyzed data it can be stated that the genre 'Film-Noir' has the highest rating
                and the most common words by %_occurrence are: 'new', 'young', 'life'.""")
        st.subheader('3. What would you change if you need to do another EDAproject?')
        st.write("""The data mining should be more specific. 
                There was not a clear goal at the beggining and valuable time was wasted on this particular task.
                Furthermore, the results would be more reliable if more data was gathered.
                """)
        st.subheader('4. What did you learn doing this project?')
        st.write("""Specify as much as possible the objective of the project and what is needed to reach that purpose.
                """)