import os, sys
import numpy as np
import random

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam, RMSprop

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root)

from src.utils.mining_data_tb import Preprocessor

###########################################################################################################################################

class LSTM_Generator(Preprocessor):

    def __init__(self, df, maxlen=40, step=3, option='character', min_word_frequency=3, model_type=1):
        """Class for creating a LSTM Model.
            - Args:
                - df: Base Quote Dataframe.
                - maxlen: Sequence length into which the corpus is divided. This will result in the number of rows of each X array.
                - step: Affects the number of sequences to be generated.
                - option: 'character' for character-based models and 'word' for word-based models.
                - min_word_frequency: Minimum word frequency to take into account when creating the word dictionary. 
                                    Affects the number of columns
                - model_type: 1 for basic LSTM and 2 for Bidirectional LSTM.
        """
        Preprocessor.__init__(self, df)
        self.maxlen = maxlen
        self.step = step
        self.option = option

        self.preprocess(maxlen=self.maxlen, step=self.step, option=option, mode='base', min_word_frequency=min_word_frequency)

        self.model = self.base_model(model_type=model_type)

    def base_model(self, model_type=1):
        """Returns a basic or bidirectional LSTM model."""

        if model_type == 1:
            model = keras.Sequential([
                layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
                layers.LSTM(128),
                layers.Dense(len(self.tokens), activation="softmax")
            ])

        if model_type == 2:
            model = keras.Sequential([
                layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
                layers.Bidirectional(layers.LSTM(128)),
                layers.LeakyReLU(alpha=0.3),
                layers.Dropout(0.3),
                layers.Dense(len(self.tokens), activation="softmax")
            ])

        model.summary()
        optimizer = RMSprop(learning_rate=0.01)
        model.compile(loss="categorical_crossentropy", optimizer=optimizer, metrics=["RootMeanSquaredError"])


        return model

    def train(self, epochs=1, batch_size=128):
        """Trains model.
            - Args:
                - epochs: Number of epochs.
                - batch_size: number of input arrays to be used in each epoch."""

        print(f'Training {self.option} LSTM model for [epochs:{epochs}, batch_size:{batch_size}]')
        self.model.fit(self.X, self.Y, batch_size=batch_size, epochs=epochs)
        print('Finished training.')

    def predict(self, option='character', quote_len=40, sentence=False, temperature=1.0, verbose=False):
        """Returns a prediction:
            - Args:
                - option: 'character' for character-based models and 'word' for word-based models.
                - quote_len: Number of characters/words to show in output. Only affects LSTM models.
                - sentence: Input string. If false, the model predicts with a random input.
                - temperature: Sequence variance distortion. Recommended low values for character based models.
                - verbose: If True, prints generations steps."""

        prediction = self.generate(self.model, mode='base', option=option, quote_len=quote_len, 
                                    sentence=sentence, temperature=temperature, verbose=verbose)

        return prediction

    def save_model(self, filepath):
        """Saves model into desired path."""

        self.model.save(filepath)
        print('Model saved.')

###########################################################################################################################################

class GAN(Preprocessor):

    def __init__(self, df, maxlen=40, step=3, option='character', min_word_frequency=3):
        """Class for creating a LSTM Model.
            - Args:
                - df: Base Quote Dataframe.
                - maxlen: Sequence length into which the corpus is divided. This will result in the number of rows of each X array.
                - step: Affects the number of sequences to be generated.
                - option: 'character' for character-based models and 'word' for word-based models.
                - min_word_frequency: Minimum word frequency to take into account when creating the word dictionary. 
                                    Affects the number of columns
        """
        Preprocessor.__init__(self, df)
        self.maxlen = maxlen
        self.step = step
        self.option = option
        self.disc_loss = []
        self.gen_loss = []

        self.preprocess(maxlen=self.maxlen, step=self.step, option=option, mode='gan', min_word_frequency=min_word_frequency)
        
        optimizer = Adam(learning_rate=0.0002, beta_1=0.5)

        # Build and compile the discriminator
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

        # Build the generator
        self.generator = self.build_generator()

        # For the combined model we will only train the generator
        self.discriminator.trainable = False

        # Build the GAN Model
        self.gan = self.build_gan(self.generator, self.discriminator)
        self.gan.compile(loss='binary_crossentropy', optimizer=optimizer)

    def get_latent_points(self, n_samples):
        """Returns a random Latent Point array."""

        x_input = np.zeros((n_samples, self.maxlen, len(self.tokens)))

        for i, element in enumerate(x_input):
            for j, row in enumerate(element):
                number = random.randint(0, len(row))
                for k in range(len(row)):
                    if k == number:
                        x_input[i][j][k] = 1

        return x_input


    def generate_fake_samples(self, model, n_samples):
        """Returns a latent point array labeled as fake samples."""

        x_input = self.get_latent_points(n_samples)

        X_fake = model.predict(x_input, verbose=0)
        y_fake = np.zeros(n_samples)

        return X_fake, y_fake

    def generate_real_samples(self, n_samples):
        """Returns real sequence arrays labeled as real samples."""

        X_true = np.array(random.sample(list(self.X), n_samples))
        y_true = np.ones(n_samples)

        return X_true, y_true

    def generate_gan_samples(self, n_samples):
        """Returns a latent point array labeled as real samples."""

        X_gan = self.get_latent_points(n_samples)
        y_gan = np.ones(len(X_gan))

        return X_gan, y_gan

    def build_discriminator(self):
        """Returns a discriminator model with the [Convolution -> LeakyRelu -> Dropout] Layer Layout."""

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

    def build_generator(self):
        """Returns a generator model with the [Dense -> LeakyRelu -> BatchNormalization] Layer Layout."""

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
        """Returns the GAN model."""

        gan = keras.Sequential([
            layers.InputLayer(input_shape=(self.maxlen, len(self.tokens))),
            g_model,
            d_model
        ])
        gan.summary()

        return gan


    def train(self, epochs, batch_size=128, sample_interval=50, verbose=True):
        """Trains the GAN model.
            - Args:
                - epochs: Number of epochs
                - batch_size: For each epoch, the whole data is divided into batches of the desired size.
                - sample interval: Number of trains before printing the metrics.
                - verbose: 1 for printing the sample interval and 2 or more for printing training steps."""

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
        """Returns a prediction:
            - Args:
                - option: 'character' for character-based models and 'word' for word-based models.
                - quote_len: Number of characters/words to show in output. Only affects LSTM models.
                - sentence: Input string. If false, the model predicts with a random input.
                - temperature: Sequence variance distortion. Recommended low values for character based models.
                - verbose: If True, prints generations steps."""

        prediction = self.generate(self.generator, mode='gan', option=option, quote_len=quote_len, 
                                    sentence=sentence, temperature=temperature, verbose=verbose)

        return prediction

    def get_mean_scores(self):
        """Returns Mean Loss and Accuracy for real and fake samples"""
        gan_loss = (self.disc_loss[-1][0][0] + self.disc_loss[-1][1][0])/2
        gan_acc = (self.disc_loss[-1][0][1] + self.disc_loss[-1][1][1])/2

        return gan_loss, gan_acc

    def save_model(self, filepath):
        """Saves model into desired location."""

        self.generator.save(filepath)
        print('GAN Generator model saved.')