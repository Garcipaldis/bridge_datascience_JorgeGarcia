import streamlit as st
import pandas as pd
from PIL import Image
import os, sys
import requests

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.visualization_tb import Visualizer
from src.utils.apis_tb import FlaskFuncs

dfpath = root + os.sep + 'data' + os.sep + 'BASE.csv'
df = pd.read_csv(dfpath)
settings_file = root + os.sep + 'src' + os.sep + "utils" + os.sep + "settings_sql.json"

class StreamFuncs(FlaskFuncs):

    def __init__(self, df, root):
        # Vizualizer class instance
        self.viz = Visualizer(df)
        self.root = root

    def greet(self):
        """Method returning a streamlit text template.
        """
        st.title('Text Generation Machine Learning Project (GAN-Dalf)')
        st.subheader('Project made by: Jorge García Navarro')
        st.write("""Text Generation is currently one of the most challenging fields in the Artificial Intelligence spectrum. 
                    The purpose of this project is to generate memorable movie quotes by the use of Natural Language Processing tecniques, 
                    Long-Short-Term Memory neural networks and Generative Adversarial Networks. 
                    The results of this investigation serves as an introduction to the complexity of the matter at hand, 
                    revealing interesting new paths for future projects.""")
        st.subheader('Memorable Quote Example')
        st.write("""If by my life or death I can protect you, I will. You have my sword.""")
        st.write('Title: The Fellowship of the Ring')

    def barchart_page(self):
        """ Returns word stats barchart on a template.
        """
        st.title('Text Generation Machine Learning Project (GAN-Dalf)')
        self.viz.get_word_popularity()
        top = st.sidebar.select_slider("Top Values",
                                        options=range(3, 21),
                                        value=10)
        horizontal = st.sidebar.checkbox('Horizontal')
        if horizontal:
            st.pyplot(self.viz.plot_word_barchart(top=top))
        else:
            st.pyplot(self.viz.plot_word_barchart(x='word', y='count',top=top, sort=1, show_values=True))

    def flask_page(self):
        """ Connects to the Flask API and returns the response json on a template.
        """
        st.title('Text Generation Machine Learning Project (GAN-Dalf)')
        r = requests.get(url="http://localhost:6060/info?token_id=B53814652")
        response = r.json()
        show_json = st.sidebar.checkbox('Show returned Json')
        df = pd.DataFrame(response).dropna()
        df.drop('Unnamed: 0', axis=1, inplace=True)
        if show_json:
            st.write(response)
        else:
            st.dataframe(df)

    def model_page(self):
        st.title('Text Generation Machine Learning Project (GAN-Dalf)')
        self.models = self.get_models()
        model = st.sidebar.selectbox('Select Model:', options=os.listdir(self.root + os.sep + 'models'))
        quote_length = st.sidebar.select_slider('Quote Length:', options=range(1, 101), value=40)
        st.subheader('Type input text. Leave blank for random')
        sentence = st.text_input('Input your sentence here (min 40 characters):', value=False)
        st.subheader('Prediction')
        st.write(self.get_predicction(model, string=sentence))

    def conclude(self):
        """ Conclusions on a template.
        """
        st.title('Text Generation Machine Learning Project (GAN-Dalf)')
        st.subheader('1. Was it possible to demonstrate the hypothesis? Why?')
        st.write("""After many data transformations on the Base Dataset, it was possible to find an answer to the stated hypothesis. 
                The analyzed data showed not only that the best rated genre was Film-Noir instead of Drama, 
                but neither 'murder' nor 'vengeance' were in the top 20.""")
        st.subheader('2. What can you conclude about your data study?')
        st.write("""Based on the analyzed data it can be stated that the genre 'Film-Noir' has the highest rating
                and the most common words by %_occurrence are: 'new', 'young', 'life'.""")
        st.subheader('3. What would you change if you need to do another EDAproject?')
        st.write("""The data mining should be more specific. 
                There was not a clear goal at the beginning and valuable time was wasted on this particular task.
                Furthermore, the results would be more reliable if more data was gathered.
                """)
        st.subheader('4. What did you learn doing this project?')
        st.write("""To specify as much as possible the objective of the project and what is needed to reach that purpose.
                """)