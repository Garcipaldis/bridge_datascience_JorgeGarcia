import numpy as np
import random
import re
import string

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam, RMSprop

class Preprocessor:

    def __init__(self, df):
        self.data = df

    def get_corpus(self, quote_list):
        # Corpus
        text = ''
        for q in quote_list:
            text += ' ' + q
        print("Corpus length:", len(text))
        
        return text.lower()


    def preprocess(self, maxlen=40, step=3, column='quote', option='character', mode='base', min_word_frequency=2):

        self.maxlen = maxlen

        # Quote List
        input_list = list(self.data[column])

        # Corpus
        text = self.get_corpus(input_list)

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
            for k, v in word_freq.items():
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
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype("float64")
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate(self, model, mode='base', option='character', quote_len=40, sentence=False, temperature=1.0, verbose=False):
        
        if verbose:
            print("...Temperature:", temperature)

        generated = ""
        if sentence == False:
            start_index = random.randint(0, len(self.text) - self.maxlen - 1)
            sentence = self.text[start_index : start_index + self.maxlen]
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

    def get_latent_points(self, n_samples):

        x_input = np.zeros((n_samples, self.maxlen, len(self.tokens)))

        for i, element in enumerate(x_input):
            for j, row in enumerate(element):
                number = random.randint(0, len(row))
                for k in range(len(row)):
                    if k == number:
                        x_input[i][j][k] = 1

        return x_input


    def generate_fake_samples(self, model, n_samples):

        x_input = self.get_latent_points(n_samples)

        X_fake = model.predict(x_input, verbose=0)
        y_fake = np.zeros(n_samples)

        return X_fake, y_fake

    def generate_real_samples(self, n_samples):

        X_true = np.array(random.sample(list(self.X), n_samples))
        y_true = np.ones(n_samples)

        return X_true, y_true

    def generate_gan_samples(self, n_samples):

        X_gan = self.get_latent_points(n_samples)
        y_gan = np.ones(len(X_gan))

        return X_gan, y_gan

class LSTM_Generator(Preprocessor):

    def __init__(self, df, maxlen=40, step=3, option='character', min_word_frequency=2):
        Preprocessor.__init__(self, df)
        self.maxlen = maxlen
        self.step = step

        self.preprocess(maxlen=self.maxlen, step=self.step, option=option, mode='base', min_word_frequency=min_word_frequency)

        self.model = self.base_model()

    def base_model(self):
        model = keras.Sequential([
            layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
            layers.LSTM(128),
            layers.Dense(len(self.tokens), activation="softmax")
        ])

        model.summary()
        optimizer = RMSprop(learning_rate=0.01)
        model.compile(loss="categorical_crossentropy", optimizer=optimizer)

        return model

    def predict(self, option='character', quote_len=40, sentence=False, temperature=1.0, verbose=False):
        
        if sentence:
            if option == 'character':
                sentence = sentence[:quote_len]
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
                sentence = [word for word in text_in_words if word.isalpha()][:quote_len]

        prediction = self.generate(self.model, mode='base', option=option, quote_len=quote_len, 
                                    sentence=sentence, temperature=temperature, verbose=verbose)

        return prediction

class GAN(Preprocessor):

    def __init__(self, df, maxlen=40, step=3, option='character', min_word_frequency=2, model_type=1):
        Preprocessor.__init__(self, df)
        self.maxlen = maxlen
        self.step = step

        self.preprocess(maxlen=self.maxlen, step=self.step, option=option, mode='gan', min_word_frequency=min_word_frequency)
        
        optimizer = Adam(learning_rate=0.0002)

        # Build and compile the discriminator
        self.discriminator = self.build_discriminator(mode=model_type)
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        # Build the generator
        self.generator = self.build_generator(mode=model_type)

        # For the combined model we will only train the generator
        self.discriminator.trainable = False

        # Build the GAN Model
        self.gan = self.build_gan(self.generator, self.discriminator)
        self.gan.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_discriminator(self, mode=1):

        if mode == 1:
            discriminator = keras.Sequential([
                keras.layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
                layers.LSTM(128),
                keras.layers.Dense(1, activation='sigmoid')
            ])
            discriminator.summary()

        elif mode == 2:
            discriminator = keras.Sequential([
                layers.Conv1D(filters=len(self.tokens),
                                    kernel_size=(3),
                                    input_shape=(self.maxlen, len(self.tokens)),
                                    padding='same'),
                layers.Dropout(0.25),
                layers.Dense(128),
                layers.LeakyReLU(alpha=0.3),
                layers.Dense(1, activation='sigmoid')
            ])

            discriminator.summary()

        elif mode == 3:
            discriminator = keras.Sequential([
                layers.Conv1D(filters=len(self.tokens), kernel_size=(3), input_shape=(self.maxlen, len(self.tokens)), padding='same'),
                layers.LeakyReLU(alpha=0.2),
                layers.Dropout(0.2),
                layers.Conv1D(filters=len(self.tokens), kernel_size=(3), input_shape=(self.maxlen, len(self.tokens)), padding='same'),
                layers.LeakyReLU(alpha=0.2),
                layers.Dropout(0.2),
                layers.Conv1D(filters=len(self.tokens), kernel_size=(3), input_shape=(self.maxlen, len(self.tokens)), padding='same'),
                layers.LeakyReLU(alpha=0.2),
                layers.Dropout(0.2),
                layers.Dense(1, activation='sigmoid')
            ])

            discriminator.summary()

        return discriminator

    def build_generator(self, mode=1):
        
        if mode == 1:
            generator = keras.Sequential([
                layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
                layers.LSTM(128, return_sequences=True),
                layers.Dense(len(self.tokens), activation='softmax'),
            ])
            generator.summary()

        elif mode == 2:
            generator = keras.Sequential([
                layers.Conv1D(filters=len(self.tokens),
                                    kernel_size=(3),
                                    input_shape=(self.maxlen, len(self.tokens)),
                                    padding='same'),
                layers.Dropout(0.25),
                layers.Dense(128),
                layers.LeakyReLU(alpha=0.3),
                layers.Dense(len(self.chars), activation='softmax')
            ])

            generator.summary()

        elif mode == 3:
            generator = keras.Sequential([
                layers.Dense((len(self.tokens)), input_shape=(self.maxlen, len(self.tokens))),
                layers.LeakyReLU(alpha=0.2),
                layers.BatchNormalization(momentum=0.8),
                layers.Dense(512),
                layers.LeakyReLU(alpha=0.2),
                layers.BatchNormalization(momentum=0.8),
                layers.Dense(len(self.tokens)),
                layers.LeakyReLU(alpha=0.2),
                layers.BatchNormalization(momentum=0.8),
                layers.Reshape((self.maxlen, len(self.tokens))),
                layers.Conv1DTranspose(len(self.tokens), 2, padding="same", activation='softmax')
            ])

            generator.summary()

        return generator

    def build_gan(self, g_model, d_model):

        gan = keras.Sequential([
            layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
            g_model,
            d_model
        ])
        gan.summary()

        return gan


    def train(self, epochs, batch_size=128, sample_interval=50, verbose=True):

        batch_per_epoch = len(self.X)//batch_size
        half_batch = batch_size//2
        # Training the model
        for epoch in range(epochs):

            for n in range(batch_per_epoch):

                # Training the discriminator
                # Select a random batch of character sequences
                if verbose > 1:
                    print(f'Generating real samples: {n+1}/{batch_per_epoch}')
                X_real, y_real = self.generate_real_samples(half_batch)

                # Generate a batch of fake character sequences
                if verbose > 1:
                    print(f'Generating fake samples: {n+1}/{batch_per_epoch}')
                X_fake, y_fake = self.generate_fake_samples(self.generator, half_batch)

                # Train the discriminator
                if verbose > 1:
                    print(f'Training Discriminator: {n+1}/{batch_per_epoch}')
                d_loss_real = self.discriminator.train_on_batch(X_real, y_real)
                d_loss_fake = self.discriminator.train_on_batch(X_fake, y_fake)
                #d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

                #  Training the Generator
                if verbose > 1:
                    print(f'Generating GAN samples: {n+1}/{batch_per_epoch}')
                X_gan, y_gan = self.generate_gan_samples(batch_size)

                # Train the generator (to have the discriminator label samples as real)
                if verbose > 1:
                    print(f'Training Generator: {n+1}/{batch_per_epoch}')
                g_loss = self.gan.train_on_batch(X_gan, y_gan)

                # Print the progress and save into loss lists
                if epoch % sample_interval == 0 and verbose > 0:
                    print(f"{epoch}:{n+1}/{batch_per_epoch}: [DR_acc: {round(d_loss_real[1],3)}, DF_acc: {round(d_loss_fake[1],3)}] [G loss: {g_loss}]")
                    self.disc_loss.append((d_loss_real, d_loss_fake))
                    self.gen_loss.append(g_loss)

    def predict(self, option='character', quote_len=40, sentence=False, temperature=1.0, verbose=False):
        
        if sentence:
            if option == 'character':
                sentence = sentence[:quote_len]
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
                sentence = [word for word in text_in_words if word.isalpha()][:quote_len]

        prediction = self.generate(self.generator, mode='gan', option=option, quote_len=quote_len, 
                                    sentence=sentence, temperature=temperature, verbose=verbose)

        return prediction