from tensorflow import keras
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Dropout
from keras import optimizers
from sklearn.model_selection import train_test_split
import numpy as np
from keras.utils import to_categorical
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support


# 26
def create_optimized_model(num_time_series_features):
    # Input for time-series features
    time_series_input = Input(shape=(None, num_time_series_features))

    # LSTM layers for time-series input
    x = LSTM(75, return_sequences=True)(time_series_input)  # lstm_units_0
    x = Dropout(0.3)(x)  # lstm_dropout_0

    x = LSTM(55)(x)  # lstm_units_1
    x = Dropout(0.4)(x)  # lstm_dropout_1

    # Dense layer
    x = Dense(200, activation="relu")(x)  # dense_units_0

    # Output layer
    output = Dense(2, activation="softmax")(x)

    # Create the model
    model = Model(inputs=[time_series_input], outputs=output)

    # Optimizer with the specified learning rate
    optimizer = optimizers.Adam(lr=0.0004247879117781972)

    # Compile the model
    model.compile(
        optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model


# Create the model

X, y = np.load("XC.npy"), np.load("yC.npy")

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = create_optimized_model(X.shape[2])
# Second split: Splitting the temporary data into 50% validation and 50% test data
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42
)


from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
class_weight_dict = dict(enumerate(class_weights))

y_train, y_val, y_test = y = (
    to_categorical(y_train, num_classes=2),
    to_categorical(y_val, num_classes=2),
    to_categorical(y_test, num_classes=2),
)

history = model.fit(
    X_train,
    y_train,
    epochs=50,
    batch_size=32,
    validation_data=(X_val, y_val),
    verbose=1,
    class_weight=class_weight_dict,
)
test_loss = model.evaluate(X_test, y_test)
y_pred = model.predict(X_test)

y_argmax_test, y_argmax_pred = (
    [np.argmax(x) for x in y_test],
    [np.argmax(x) for x in y_pred],
)
print(confusion_matrix(y_argmax_test, y_argmax_pred))


print(precision_recall_fscore_support(y_argmax_test, y_argmax_pred))

feature_extractor = keras.Model(
    inputs=model.inputs,
    outputs=model.layers[-2].output,  # Output from the layer before the last one
)

last_layer = model.layers[-1]
weights, biases = last_layer.get_weights()

logit_input = keras.Input(shape=(feature_extractor.output.shape[1],))
# Create the dense layer (assuming the last layer is a dense layer)
new_dense_layer = keras.layers.Dense(
    units=last_layer.units, activation=last_layer.activation
)

# Set the weights

# Create the new model
classifier = keras.Model(inputs=logit_input, outputs=new_dense_layer(logit_input))
# single_ts_sample = X_test[0].reshape(1, -1, 1)  # Reshape time series data
new_dense_layer.set_weights([weights, biases])

logits = feature_extractor.predict(X_test[0][np.newaxis, :])

# Step 2: Classify the logits using the classifier
prediction = classifier.predict(logits)

# Output the prediction
print("Prediction:", prediction)

classifier.save("zscore_classifier.h5")
model.save("zscore_complete.h5")
