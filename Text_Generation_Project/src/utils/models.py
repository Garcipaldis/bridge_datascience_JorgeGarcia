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
        
        return text.lower()

    def preprocess(self, maxlen=40, step=3, column='quote'):

        self.maxlen = maxlen

        # Quote List
        input_list = list(self.data[column])

        # Corpus
        text = self.get_corpus(input_list)

        # Total Characters
        chars = sorted(list(set(text)))
        print("Total chars:", len(chars))

        # Dictionaries
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))

        # Number of sequences
        sentences = []
        next_chars = []
        for i in range(0, len(text) - maxlen, step):
            sentences.append(text[i : i + maxlen])
            next_chars.append(text[i + maxlen])
        print("Number of sequences:", len(sentences))

        # Defining X and y
        x = np.zeros((len(sentences), maxlen, len(chars)))
        y = np.zeros((len(sentences), len(chars)))
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1

        self.text = text
        self.chars = chars
        self.char_indices = char_indices
        self.indices_char = indices_char
        self.sentences = sentences
        self.next_chars = next_chars
        self.X = x
        self.Y = y

    def sample(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate(self, model, option=1, quote_len=40, sentence=False, temperature=1.0, verbose=False, fake=False):
        
        if verbose:
            print("...Temperature:", temperature)

        generated = ""
        if fake == True:
            sentence = random.choices(self.chars, k=self.maxlen)
            sentence = ''.join(sentence)
        elif sentence == False:
            start_index = random.randint(0, len(self.text) - self.maxlen - 1)
            sentence = self.text[start_index : start_index + self.maxlen]
        if verbose:
            print('...Generating with seed: "' + sentence + '"')

        if option == 1:
            for i in range(quote_len):
                x_pred = np.zeros((1, self.maxlen, len(self.chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, self.char_indices[char]] = 1.0 #One-Hot Array
                preds = model.predict(x_pred, verbose=0)[0]
                next_index = self.sample(preds, temperature)
                next_char = self.indices_char[next_index]
                sentence = sentence[1:] + next_char
                generated += next_char

        elif option == 2:
            x_pred = np.zeros((1, self.maxlen, len(self.chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, self.char_indices[char]] = 1.0 #One-Hot Array
            preds = model.predict(x_pred, verbose=0)[0]
            for pred in list(preds):
                next_index = self.sample(pred, temperature=1)
                next_char = self.indices_char[next_index]
                generated += next_char

        if verbose:
            print("...Generated: ", generated)

        return generated

    def generate_fake_samples(self, model, n_samples, quote_len=40, temperature=1.0):

        x_random = []
        for n in range(n_samples):
            x_random.append(self.generate(model, option=2, quote_len=quote_len, temperature=temperature, fake=True))

        X_fake = np.zeros((len(x_random), self.maxlen, len(self.chars)))
        for i, sentence in enumerate(x_random):
            for t, char in enumerate(sentence):
                X_fake[i, t, self.char_indices[char]] = 1

        #X_fake = X_fake.reshape(X_fake.shape[0], X_fake.shape[1], X_fake.shape[2], 1)
        y_fake = np.zeros(n_samples)

        return X_fake, y_fake

    def generate_real_samples(self, n_samples):

        X_true = np.array(random.sample(list(self.X), n_samples))
        #X_true = X_true.reshape(X_true.shape[0], X_true.shape[1], X_true.shape[2], 1)
        y_true = np.ones(n_samples)

        return X_true, y_true

    def generate_gan_samples(self, n_samples):

        sample_list = random.sample(range(len(self.X)), n_samples)

        X_gan = self.X[sample_list]
        y_gan = np.ones(len(X_gan))

        return X_gan, y_gan

    def generate_disc_inputs(self, model, n_samples, quote_len=40, temperature=1):

        sample_list = random.sample(self.sentences, n_samples)

        predictions = []
        for seq in sample_list:
            predictions.append(self.generate(model, quote_len=quote_len, temperature=temperature, sentence=seq))

        # Defining X and y
        x_input = np.zeros((len(predictions), self.maxlen, len(self.chars)))
        for i, sentence in enumerate(predictions):
            for t, char in enumerate(sentence):
                x_input[i, t, self.char_indices[char]] = 1

        return x_input

    def preprocess_type2(self, maxlen=40, step=3, column='quote'):

        self.maxlen = maxlen

        # Quote List
        input_list = list(self.data[column])

        # Corpus
        text = self.get_corpus(input_list)

        # Total Characters
        chars = sorted(list(set(text)))
        print("Total chars:", len(chars))

        # Dictionaries
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))

        # Number of sequences
        sentences = []
        next_seq = []
        for i in range(0, len(text) - 2*maxlen, step):
            sentences.append(text[i : i + maxlen])
            next_seq.append(text[i + maxlen:i + 2*maxlen])
        print("Number of sequences:", len(sentences))

        # Defining X and y
        x = np.zeros((len(sentences), maxlen, len(chars)))
        y = np.zeros((len(sentences), maxlen, len(chars)))
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_indices[char]] = 1
                y[i, t, char_indices[next_seq[i][t]]] = 1

        self.text = text
        self.chars = chars
        self.char_indices = char_indices
        self.indices_char = indices_char
        self.sentences = sentences
        self.next_chars = next_seq
        self.X = x
        self.Y = y