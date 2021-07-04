import numpy as np
import random


class CharacterPreprocessor:

    def __init__(self, df):
        self.data = df

    def get_corpus(self, quote_list):
        # Corpus
        text = ''
        for q in quote_list:
            text += ' ' + q
        print("Corpus length:", len(text))
        
        self.text = text.lower()
        return text
        

    def preprocess(self, maxlen=40, step=3, column='quote'):

        self.maxlen = maxlen

        # Quote List
        quotes = list(self.data[column])

        # Corpus
        self.get_corpus(quotes)

        # Total Characters
        chars = sorted(list(set(self.text)))
        print("Total chars:", len(chars))
        self.chars = chars

        # Dictionaries
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))
        self.char_indices = char_indices
        self.indices_char = indices_char

        # Number of sequences
        sentences = []
        next_chars = []
        for i in range(0, len(self.text) - maxlen, step):
            sentences.append(self.text[i : i + maxlen])
            next_chars.append(self.text[i + maxlen])
        print("Number of sequences:", len(sentences))

        # Defining X and y
        x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1

        self.X = x
        self.Y = y

        return x, y

    def sample(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate(self, model, quote_len=400, temperature=1.0):
        
        print("...Temperature:", temperature)

        generated = ""
        start_index = random.randint(0, len(self.text) - self.maxlen - 1)
        sentence = self.text[start_index : start_index + self.maxlen]
        print('...Generating with seed: "' + sentence + '"')

        for i in range(quote_len):
            x_pred = np.zeros((1, self.maxlen, len(self.chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, self.char_indices[char]] = 1.0
            preds = model.predict(x_pred, verbose=0)[0]
            next_index = self.sample(preds, temperature)
            next_char = self.indices_char[next_index]
            sentence = sentence[1:] + next_char
            generated += next_char

        print("...Generated: ", generated)

        return generated