import os
import joblib
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from file_handling import (
    read_metadata,
    read_data,
)
from utils.encoding import (
    one_hot_encode,
    ordinal_encode,
)
from utils.pipeline import run_training


CLASSIFIERS_MAPPING = {
    'knn': KNeighborsClassifier(n_neighbors=3),
    'gaussian': GaussianNB(),
}
CLASSIFIER_NAME = os.getenv('KONAN_MODEL_CLASSIFIER_NAME')
ARTIFACTS_PATH = os.getenv(
    'KONAN_MODEL_ARTIFACTS_PATH',
    f'artifacts/{CLASSIFIER_NAME}',
)


# ------------------------------------------------------------------- #
# Read the files
train, _ = read_data()
metadata = read_metadata()
# print("Train set size:", train.shape)


# ------------------------------------------------------------------- #
y_train: pd.Series = train['survived'].map({"no": 0, "yes": 1})


# ------------------------------------------------------------------- #
X_train = train.copy().drop(
    ['survived'],
    axis=1,
)
print("Train Features:", X_train.shape)

# ------------------------------------------------------------------- #
# One-Hot-Encode Categorical Features
X_train, one_hot_encoder = one_hot_encode(
    df=X_train,
    columns=metadata['oneHotEncoding'],
    encoder=None,
)
print("Train Features after one-hot-encoding set size:", X_train.shape)

# ------------------------------------------------------------------- #
# Label-Encode Ordinal Features
X_train, ordinal_encoder = ordinal_encode(
    df=X_train,
    columns=list(metadata['ordinalEncoding'].keys()),
    categories=list(metadata['ordinalEncoding'].values()),
    encoder=None,
)
print("Train Features after ordinal-encoding set size:", X_train.shape)

# ------------------------------------------------------------------- #
# Fill all remaining NAs
X_train = X_train.fillna(0)


# # ------------------------------------------------------------------- #
# # Train and test the model

print(CLASSIFIER_NAME)
fit_classifier = run_training(
    classifier_name=CLASSIFIER_NAME,
    classifier=CLASSIFIERS_MAPPING.get(CLASSIFIER_NAME, None),
    X_train=X_train,
    y_train=y_train,
)


# # ------------------------------------------------------------------- #
# # Save model artifacts

joblib.dump(
    fit_classifier,
    f'{ARTIFACTS_PATH}/model.pkl',
)
joblib.dump(
    one_hot_encoder,
    f'{ARTIFACTS_PATH}/one_hot_encoder.pkl',
)
joblib.dump(
    ordinal_encoder,
    f'{ARTIFACTS_PATH}/ordinal_encoder.pkl',
)
