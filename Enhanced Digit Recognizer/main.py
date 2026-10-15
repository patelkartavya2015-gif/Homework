import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train.astype("float32")[..., None] / 255.0
x_test = x_test.astype("float32")[..., None] / 255.0

augmentation = models.Sequential([
    layers.RandomRotation(0.05),
    layers.RandomTranslation(0.08, 0.08),
    layers.RandomZoom(0.08),
], name="data_augmentation")

model = models.Sequential([
    layers.Input(shape=(28, 28, 1)),
    augmentation,
    layers.Conv2D(32, 3, padding="same"),
    layers.LeakyReLU(negative_slope=0.1),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding="same"),
    layers.LeakyReLU(negative_slope=0.1),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128),
    layers.LeakyReLU(negative_slope=0.1),
    layers.Dropout(0.3),
    layers.Dense(10, activation="softmax"),
])

model.compile(
    optimizer=tf.keras.optimizers.RMSprop(learning_rate=0.001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    patience=2,
    restore_best_weights=True,
)

history = model.fit(
    x_train,
    y_train,
    epochs=12,
    batch_size=128,
    validation_split=0.1,
    callbacks=[early_stopping],
)

test_loss, test_acc = model.evaluate(x_test, y_test)
print(f"\nTest accuracy: {test_acc:.4f}")
print(f"Test loss: {test_loss:.4f}")

predictions = model.predict(x_test, verbose=0)
predicted_labels = predictions.argmax(axis=1)

figure, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history.history["accuracy"], label="Training")
axes[0].plot(history.history["val_accuracy"], label="Validation")
axes[0].set_title("Accuracy")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("Accuracy")
axes[0].legend()

axes[1].plot(history.history["loss"], label="Training")
axes[1].plot(history.history["val_loss"], label="Validation")
axes[1].set_title("Loss")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Loss")
axes[1].legend()
figure.tight_layout()

figure, axes = plt.subplots(4, 5, figsize=(10, 8))
for index, axis in enumerate(axes.flat):
    axis.imshow(x_test[index].squeeze(), cmap="binary")
    color = "green" if predicted_labels[index] == y_test[index] else "red"
    axis.set_title(
        f"Pred: {predicted_labels[index]} | True: {y_test[index]}",
        color=color,
        fontsize=9,
    )
    axis.axis("off")
figure.tight_layout()
plt.show()