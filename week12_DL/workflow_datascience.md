1. Tema/Hipótesis 
2. Datos - ¿Existen suficientes datos? 
    2.1 Conseguir más datos
3. EDA: (creación de semilla)
    * Si se precisa crear baseline, pasar a \\7. haciendo los pasos básicos de EDA para que sea posible.

    3.0. Data Wrangling
    3.1. Visualizar los datos / comprender los datos
    Data Mining
    3.2. Limpiar datos: NaN, duplicados, eliminar columnas no relevantes,...
    3.3. Encoder/get_dummies
    3.4. Normalizar [-1, 1], Scalar media = 0, var = 1
    3.5. Outliers?
    3.6. Añadir columnas (mediana, media, varianza, covarianza...) / generar rangos (pd.cut)
    3.7. Reducción de la dimensionalidad, PCA, T-sne (...)
    \\3.8. Eliminar columnas conileanes*
    3.9. Repetir proceso hasta diferentes versiones.
    3.10. Preprocesamiento de datos (data augmentation)
    https://machinelearningmastery.com/how-to-configure-image-data-augmentation-when-training-deep-learning-neural-networks/
4. Creación del conjunto de entrenamiento y de test
5. Elegir el modelo y parámetros 
    5.1. No deep learning (GridSearch opcional)
    5.2. Con deep learning:
        5.2.1. Arquitectura: podemos elegir diferentes capas para nuestra red neuronal (convolución, dense, rnn, flaten, embedding(NLP),maxpool,(...)).
        5.2.2. En cada capa tenemos: neuronas, función de activación (relu, sigmoid, linear, tanh, softmax [para la última capa ya que saca valores entre 0 y 1|| usado en clasificación])
        5.2.3. Función de optimización: altera la forma en la que la red aprende(adam, adadelta, rmsprop,(...)) con una serie de parámetros (learning_rate). Podemos agregar regularización añadiendo capas de dropout y L1, L2, (...)
        https://towardsdatascience.com/machine-learning-model-regularization-in-practice-an-example-with-keras-and-tensorflow-2-0-52a96746123e
        \\Dense(64, kernel_regularizer=l2(0.01))
        5.2.4. Callbacks: Podemos agregar diferentes formas de monitorizar el entrenamiento. EarlyStop trata de parar el entrenamiento si detecta sobreentrenamiento. Podemos cambiar la forma en la que se va mostrando la información en cada epoch/batch (FuntionDot -- nombre de clase). 
        5.2.5. Métricas: debemos especificar a partir de qué parámetro nuestra red va a tratar de mejorar. Normalmente se debe especificar el loss de entrenamiento. 
            5.2.5.1. En los problemas de regresión, normalmente se utiliza rmse, mse, mae. En clasificación se utiliza alguna forma de accuracy (accuracy, roc-auc, f1-score, precision, recall, r2)
        \\logit -> [200, 400]
        \\logic_real -> [100, 400]
        \\softmax -> [0.25, 0.75]
        \\softmax_real -> [0, 1]

6. Entrenar el modelo (X_train): 
    6.1 Entrenar con todos los datos sin cross validation
    6.2 Cross validation normal (warm_start=True)
    6.3 Cross validation poco a poco (partiendo en pequeños trozos)(warm_start)  
\\7. Creación del modelo baseline entrenado (este modelo es simplemente el modelo de partida para futuras comparaciones). Lo primero que habría que hacer a nivel teórico crear un baseline para tener una referencia. Nos tenemos que quedar con un score para poder comparar.
    7.1 Repetir 3,4,5,6 eligiendo un modelo mejor.
8. Sacar el score con el conjunto de test
    8.1 volver al punto 2/3 para intentar encontrar la mejor relación de los datos
9. Si nuestro score es correcto y tenemos la necesidad de probar nuestro modelo para el mayor conjunto de datos, sería conveniente probar nuestras modificaciones y algoritmo con diferentes semillas aleatorias para comprobar el rendimiento real de nuestro modelo.
10. Si todo OK -- Entrenar con todos los datos (X).
11. Guardamos el modelo
12. Usar el modelo en producción (desplegar el modelo)
13. Monitorizar el modelo