import pandas as pd
import os

import numpy as np
import random
import re
import string

from tensorflow import keras

extra_quotes = {
        'the lord of the rings: the fellowship of the ring': ['A wizard is never late, Frodo Baggins. Nor is he early. He arrives precisely when he means to.',
        'You shall not pass!',
        'Fly you fools!',
        'Even the smallest person can change the course of the future.',
        'Many that live deserve death. Some that die deserve life...Do not be too eager to deal out death in judgement. Even the very wise cannot see all ends.',
        'So do all who live to see such times. But that is not for them to decide. All we have to decide is what to do with the time that is given to us.',
        'One ring to rule them all. One ring to find them. One ring to bring them all and in the darkness bind them!',
        'If by my life or death I can protect you, I will. You have my sword'],
        'the lord of the rings: the return of the king': ["Certainty of death. Small chance of success. What are we waiting for?",
            "The journey doesn't end here. Death is just another path... One that we all must take.",
            "I see in your eyes the same fear that would take the heart of me.",
            "But it is not this day!"]
            }

######################################################################################################################################################

class QuoteCleaner:
    """ Class designed for basic transformation on input dataframe or .txt file."""

    def __init__(self, filepath):
        self.df = self.create_quote_dataset(filepath)

    def create_quote_dataset(self, filepath):
        """Reads .txt file containing the memorable quotes and returns a dataframe."""
        with open(filepath, 'r') as raw:
            text = raw.readlines()
            lista = [line for line in text if line != '\n']
        
        data = {}
        data['title'] = [lista[i].strip('\n') for i in range(0, len(lista), 3)]
        data['quote'] = [lista[i].strip('\n') for i in range(1, len(lista), 3)]

        return pd.DataFrame(data, index=range(len(data['title'])))

    def add_quotes(self, extra_quotes):
        """Adds input dictionary of quotes into the dataframe."""
        for title, quotes in extra_quotes.items():
            for quote in quotes:
                self.df = self.df.append({'title':title, 'quote':quote}, ignore_index=True)

    def save_quote_df(self, path):
        """Saves dataframe into desired location."""
        self.df.to_csv(path)
        print('Successfully saved Dataframe.')

    def clean_text(self, dirpath, name):
        """For creating a corpus text."""
        with open(dirpath + os.sep + name, 'r') as raw:
            corpus = raw.readlines()
        lines = [line.replace('\n','') for line in corpus]
        lines = [line.replace('     ','') for line in lines]
        corpus = ''.join(lines)

        with open(dirpath + os.sep + 'corpus.txt', 'w') as f:
            f.write(corpus)
        print(f'Obtained corpus text from {name}')

###################################################################################################################################################

class Preprocessor:
    """Base class for all input preprocessing and basic model functions."""

    def __init__(self, input_object):
        if isinstance(input_object, str):
            self.text = input_object
            print('Corpus length:', len(self.text))
        else:
            self.data = input_object
            self.text = ''

    def get_corpus(self, quote_list):
        """Returns corpus text in lowercase from quote list."""
        text = ''
        for q in quote_list:
            text += ' ' + q
        print("Corpus length:", len(text))
        
        return text.lower()


    def preprocess(self, maxlen=40, step=3, column='quote', option='character', mode='base', min_word_frequency=3):
        """All-around preprocessor for input quote dataframe. Creates all the needed class attributes.
            - Args:
                - maxlen: Sequence length into which the corpus is divided. This will result in the number of rows of each X array.
                - step: Affects the number of sequences to be generated.
                - column: dataframe column from which to extract the quotes.
                - option: 'character' for character-based models and 'word' for word-based models.
                - mode: 'base' for LSTM models and 'gan' for GAN models.
                - min_word_frequency: Minimum word frequency to take into account when creating the word dictionary. 
                                    Affects the number of columns
        """

        self.maxlen = maxlen

        # Corpus
        if self.text == '':
            # Quote List
            input_list = list(self.data[column])
            text = self.get_corpus(input_list)
        else:
            text = self.text

        sequences = []
        next_tokens = []

        if option == 'character':
            # Total Characters
            tokens = sorted(list(set(text)))
            print("Total chars:", len(tokens))

            # Dictionaries
            token_indices = dict((c, i) for i, c in enumerate(tokens))
            indices_token = dict((i, c) for i, c in enumerate(tokens))

        elif option == 'word':
            # Clean Text
            text = re.sub('<br />', ' ', text)
                # replace '--' with a space ' '
            doc = text.replace('--', ' ')
                # split into tokens by white space
            text_in_words = doc.split()
                # remove punctuation from each token
            table = str.maketrans('', '', string.punctuation)
            text_in_words = [w.translate(table) for w in text_in_words]
                # remove '' strings
            pops = [[seq.pop(i) for i, w in enumerate(seq) if w == '' or w == ' '] for seq in text_in_words]
                # remove remaining tokens that are not alphabetic
            text_in_words = [word for word in text_in_words if word.isalpha()]
            print("Total words:", len(text_in_words))
            self.text_in_words = text_in_words

            # Calculate word frequency
            word_freq = {}
            for word in text_in_words:
                word_freq[word] = word_freq.get(word, 0) + 1

            ignored_words = set()
            for k in word_freq.keys():
                if word_freq[k] < min_word_frequency:
                    ignored_words.add(k)

            words = set(text_in_words)
            print('Unique words before ignoring:', len(words))
            print('Ignoring words with frequency <', min_word_frequency)
            tokens = sorted(set(words) - ignored_words)
            print('Unique words after ignoring:', len(tokens))

            # Dictionaries
            token_indices = dict((c, i) for i, c in enumerate(tokens))
            indices_token = dict((i, c) for i, c in enumerate(tokens))

        # Saving variables
        self.text = text
        self.tokens = tokens
        self.token_indices = token_indices
        self.indices_token = indices_token

        if mode == 'base':
            if option == 'character':
                for i in range(0, len(text) - maxlen, step):
                    sequences.append(text[i : i + maxlen])
                    next_tokens.append(text[i + maxlen])
            # In case of word-preprocessing, only add sequences where no word is in ignored_words
            elif option == 'word':
                for i in range(0, len(text_in_words) - maxlen, step):
                    if len(set(text_in_words[i: i+ maxlen + 1]).intersection(ignored_words)) == 0:
                        sequences.append(text_in_words[i : i + maxlen])
                        next_tokens.append(text_in_words[i + maxlen])
            print("Number of sequences:", len(sequences))

            # Defining X and y
            x = np.zeros((len(sequences), maxlen, len(tokens)))
            y = np.zeros((len(sequences), len(tokens)))
            for i, sentence in enumerate(sequences):
                for t, char in enumerate(sentence):
                    x[i, t, token_indices[char]] = 1
                y[i, token_indices[next_tokens[i]]] = 1

        elif mode == 'gan':
            if option == 'character':
                for i in range(0, len(text) - 2*maxlen, step):
                    sequences.append(text[i : i + maxlen])
                    next_tokens.append(text[i + maxlen:i + 2*maxlen])
            # In case of word-preprocessing, only add sequences where no word is in ignored_words
            elif option == 'word':
                for i in range(0, len(text_in_words) - 2*maxlen, step):
                    if len(set(text_in_words[i: i+ 2*maxlen + 1]).intersection(ignored_words)) == 0:
                        sequences.append(text_in_words[i : i + maxlen])
                        next_tokens.append(text_in_words[i + maxlen:i + 2*maxlen])
            print("Number of sequences:", len(sequences))

            # Defining X and y
            x = np.zeros((len(sequences), maxlen, len(tokens)))
            y = np.zeros((len(sequences), maxlen, len(tokens)))
            for i, sentence in enumerate(sequences):
                for t, char in enumerate(sentence):
                    x[i, t, token_indices[char]] = 1
                    y[i, t, token_indices[next_tokens[i][t]]] = 1

        self.sequences = sequences
        self.next_tokens = next_tokens
        self.X = x
        self.Y = y

    def sample(self, preds, temperature=1.0):
        """helper function to sample an index from a probability array"""
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate(self, model, mode='base', option='character', quote_len=40, sentence=False, temperature=1.0, verbose=False):
        """ Returns a prediction from desired model.
            - Args:
                - model: Selected keras model.
                - mode: 'base' for LSTM models and 'gan' for GAN models.
                - option: 'character' for character-based models and 'word' for word-based models.
                - quote_len: Number of characters/words to show in output. Only affects LSTM models.
                - sentence: Input string. If false, the model predicts with a random input.
                - temperature: Sequence variance distortion. Recommended low values for character based models.
                - verbose: If True, prints generations steps.
            - Returns:
                - Prediction string"""
        
        if verbose:
            print("...Temperature:", temperature)

        if sentence:
            if option == 'character':
                sentence = sentence[:self.maxlen].lower()
            elif option == 'word':
                sentence = sentence.lower()
                sentence = sentence.replace('--', ' ')
                # split into tokens by white space
                text_in_words = sentence.split()
                # remove punctuation from each token
                table = str.maketrans('', '', string.punctuation)
                text_in_words = [w.translate(table) for w in text_in_words]
                pops = [[seq.pop(i) for i, w in enumerate(seq) if w == '' or w == ' '] for seq in text_in_words]
                # remove remaining tokens that are not alphabetic
                sentence = [word for word in text_in_words if word.isalpha()][:self.maxlen]

        generated = ""
        if sentence == False:
            if option == 'character':
                start_index = random.randint(0, len(self.text) - self.maxlen - 1)
                sentence = self.text[start_index : start_index + self.maxlen]
            elif option == 'word':
                start_index = random.randint(0, len(self.tokens) - self.maxlen - 1)
                sentence = self.tokens[start_index : start_index + self.maxlen]
        if verbose:
            print('...Generating with seed: "' + sentence + '"')

        if mode == 'base':
            for i in range(quote_len):
                x_pred = np.zeros((1, self.maxlen, len(self.tokens)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, self.token_indices[char]] = 1.0 #One-Hot Array
                preds = model.predict(x_pred, verbose=0)[0]
                next_index = self.sample(preds, temperature)
                next_char = self.indices_token[next_index]
                if option == 'character':
                    sentence = sentence[1:] + next_char
                    generated += next_char
                elif option == 'word':
                    sentence = sentence[1:]
                    sentence.append(next_char)
                    generated += next_char + ' '

        elif mode == 'gan':
            x_pred = np.zeros((1, self.maxlen, len(self.tokens)))
            for t, char in enumerate(sentence):
                x_pred[0, t, self.token_indices[char]] = 1.0 #One-Hot Array
            preds = model.predict(x_pred, verbose=0)[0]
            for pred in list(preds):
                next_index = self.sample(pred, temperature=1)
                next_char = self.indices_token[next_index]
                if option == 'character':
                    generated += next_char
                elif option == 'word':
                    generated += next_char + ' '

        if verbose:
            print("...Generated: ", generated)

        return generated

    def load_model(self, model_path):
        """Loads a keras model from desired path."""

        self.model = keras.models.load_model(model_path)
        print('Model successfully loaded.')