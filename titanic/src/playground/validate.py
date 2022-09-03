import os
import joblib
import pandas as pd

from file_handling import (
    read_metadata,
    read_data,
)
from utils.encoding import (
    one_hot_encode,
    ordinal_encode,
)
from utils.pipeline import run_testing


CLASSIFIER_NAME = os.getenv('KONAN_MODEL_CLASSIFIER_NAME')
ARTIFACTS_PATH = os.getenv(
    'KONAN_MODEL_ARTIFACTS_PATH',
    f'artifacts/{CLASSIFIER_NAME}',
)


# ------------------------------------------------------------------- #
# Read the files
_, val = read_data()
metadata = read_metadata()
# print("Validation set size:", val.shape)


# ------------------------------------------------------------------- #
# Load model artifacts
classifier = joblib.load(
    f'{ARTIFACTS_PATH}/model.pkl',
)
one_hot_encoder = joblib.load(
    f'{ARTIFACTS_PATH}/one_hot_encoder.pkl',
)
ordinal_encoder = joblib.load(
    f'{ARTIFACTS_PATH}/ordinal_encoder.pkl',
)

# ------------------------------------------------------------------- #
y_val: pd.Series = val['survived'].map({"no": 0, "yes": 1,})


# ------------------------------------------------------------------- #
# Process features
X_val = val.copy().drop(
    ['survived'],
    axis=1,
)

# ------------------------------------------------------------------- #
# One-Hot-Encode Categorical Features
X_val, _ = one_hot_encode(
    df=X_val,
    columns=metadata['oneHotEncoding'],
    encoder=one_hot_encoder,
)

# ------------------------------------------------------------------- #
# Label-Encode Ordinal Features
X_val, _ = ordinal_encode(
    df=X_val,
    columns=list(metadata['ordinalEncoding'].keys()),
    categories=list(metadata['ordinalEncoding'].values()),
    encoder=ordinal_encoder,
)


# ------------------------------------------------------------------- #
# Fill all remaining NAs
X_val = X_val.fillna(0)


# ------------------------------------------------------------------- #
# Validate the model
val_accuracy = run_testing(
    classifier=classifier,
    X_test=X_val,
    y_test=y_val,
)

print(f"Model validation Accuracy Score: {val_accuracy}")
