import os
import json
import numpy as np
import tensorflow as tf

from tf.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.utils import image_dataset_from_directory


# ============================================================
# 1. CHECK TENSORFLOW AND GPU
# ============================================================

print("TensorFlow version:", tf.__version__)
print("GPU:", tf.config.list_physical_devices("GPU"))


# ============================================================
# 2. DATASET PATHS
# ============================================================

TRAIN_DIR = "/kaggle/input/plant-village/train"
VAL_DIR   = "/kaggle/input/plant-village/val"
TEST_DIR  = "/kaggle/input/plant-village/test"


# ============================================================
# 3. SETTINGS
# ============================================================

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10


# ============================================================
# 4. LOAD DATASETS
# ============================================================

train_ds = image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_ds = image_dataset_from_directory(
    VAL_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_ds = image_dataset_from_directory(
    TEST_DIR,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# 5. GET CLASS NAMES
# ============================================================

class_names = train_ds.class_names

print("\nNumber of classes:", len(class_names))

print("\nClass mapping:")

for i, class_name in enumerate(class_names):
    print(i, "->", class_name)


# ============================================================
# 6. OPTIMIZE DATA PIPELINE
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)


# ============================================================
# 7. LOAD BUILT-IN RESNET50
# ============================================================

base_model = ResNet50(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)


# ============================================================
# 8. FREEZE RESNET50
# ============================================================

base_model.trainable = False


# ============================================================
# 9. BUILD CLASSIFICATION MODEL
# ============================================================

inputs = tf.keras.Input(shape=(224, 224, 3))

x = preprocess_input(inputs)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dropout(0.3)(x)

outputs = layers.Dense(len(class_names), activation="softmax")(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs)


# ============================================================
# 10. COMPILE
# ============================================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# 11. MODEL SUMMARY
# ============================================================

model.summary()


# ============================================================
# 12. TRAIN
# ============================================================

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)


# ============================================================
# 13. TEST
# ============================================================

test_loss, test_accuracy = model.evaluate(test_ds)

print("\nTest Loss:", test_loss)
print("Test Accuracy:", test_accuracy)


# ============================================================
# 14. SAVE MODEL
# ============================================================

MODEL_PATH = "/kaggle/working/plant_disease_resnet50.keras"

model.save(MODEL_PATH)

print("\nModel saved at:")
print(MODEL_PATH)


# ============================================================
# 15. SAVE CLASS NAMES
# ============================================================

CLASS_NAMES_PATH = "/kaggle/working/class_names.json"

with open(CLASS_NAMES_PATH, "w") as f:
    json.dump(class_names, f)

print("\nClass names saved at:")
print(CLASS_NAMES_PATH)


# ============================================================
# 16. CHECK OUTPUT FILES
# ============================================================

print("\nFiles generated in /kaggle/working:")

for file in os.listdir("/kaggle/working"):
    print(file)