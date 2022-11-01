from typing import Optional
import logging
import joblib
import json
from sklearn.neighbors import KNeighborsClassifier
import yaml

from sklearn.model_selection import train_test_split
import pandas as pd

from utils.encoding import one_hot_encode, ordinal_encode
from utils.pipeline import run_testing, run_training

RETRAINING_DIR_PATH = "/retraining"
METRICS_FILE_PATH = f"{RETRAINING_DIR_PATH}/metrics.json"
ARTIFACTS_DIR_PATH = f"{RETRAINING_DIR_PATH}/artifacts"
DATA_DIR_PATH = f"{RETRAINING_DIR_PATH}/data"
TRAINING_DATA_FILE_PATH = f"{DATA_DIR_PATH}/training.csv"
SERVING_DATA_FILE_PATH = f"{DATA_DIR_PATH}/serving.csv"

LOGGER = logging.getLogger(name=__name__)


def retrain():
    # ------------------------------------------------------------------- #
    # Read the files
    LOGGER.info('Reading data files')
    training_data: Optional[pd.DataFrame] = None
    serving_data: Optional[pd.DataFrame] = None
    try:
        training_data = pd.read_csv(TRAINING_DATA_FILE_PATH)
        training_data['survived'].map({"yes": 1, "no": 0})
    except:
        pass
    try:
        serving_data = pd.read_csv(SERVING_DATA_FILE_PATH)
        serving_data['survived'].map({"yes": 1, "no": 0})
    except:
        pass

    if training_data is not None:
        LOGGER.info('Successfuly read training data %d rows and %d columns' % training_data.shape)        
    if serving_data is not None:
        LOGGER.info('Successfuly read serving data %d rows and %d columns' % serving_data.shape)
    if training_data is None and serving_data is None:
        LOGGER.error('Unable to read both training and serving data')
        return -1

    LOGGER.info('Finished reading data files')

    data = []
    if training_data is not None:
        data.append(training_data.reset_index(drop=True))
    if serving_data is not None:
        data.append(serving_data.reset_index(drop=True))

    # ------------------------------------------------------------------- #
    # Combine and split all data
    LOGGER.info('Preparing data for retraining')
    df = pd.concat(
        data,
        axis=0,
    )
    train, test = train_test_split(
        df,
        test_size=0.15,
        random_state=68,
    )

    LOGGER.info('Attempting to read required metadata file')
    with open(f'{ARTIFACTS_DIR_PATH}/metadata.yml') as file:
        metadata = yaml.safe_load(file)

    # ------------------------------------------------------------------- #
    y_train: pd.Series = train["survived"]
    y_test: pd.Series = test["survived"]

    X_train = train.drop(
        ['survived'],
        axis=1,
    )
    X_test = test.drop(
        ['survived'],
        axis=1,
    )

    LOGGER.info('Preprocessing the data')

    # ------------------------------------------------------------------- #
    # One-Hot-Encode Categorial Features
    X_train, one_hot_encoder = one_hot_encode(
        df=X_train,
        columns=metadata['oneHotEncoding'],
        encoder=None,
    )
    X_test, _ = one_hot_encode(
        df=X_test,
        columns=metadata['oneHotEncoding'],
        encoder=one_hot_encoder,
    )

    # ------------------------------------------------------------------- #
    # Label-Encode Ordinal Features
    X_train, ordinal_encoder = ordinal_encode(
        df=X_train,
        columns=list(metadata['ordinalEncoding'].keys()),
        categories=list(metadata['ordinalEncoding'].values()),
        encoder=None,
    )
    X_test, _ = ordinal_encode(
        df=X_test,
        columns=list(metadata['ordinalEncoding'].keys()),
        categories=list(metadata['ordinalEncoding'].values()),
        encoder=ordinal_encoder,
    )

    X_train = X_train.fillna(0)
    X_test = X_test.fillna(0)

    # ------------------------------------------------------------------- #
    # Train and test the model
    LOGGER.info('Beginning the retraining')
    classifier = run_training(
        classifier_name="knn",
        classifier=KNeighborsClassifier(
            n_neighbors=3,
        ),
        X_train=X_train,
        y_train=y_train,
    )
    LOGGER.info('Calculating metrics on training data')
    accuracy_train = run_testing(
        classifier=classifier,
        X_test=X_train,
        y_test=y_train,
    )
    LOGGER.info('Calculating metrics on testing data')
    accuracy_test = run_testing(
        classifier=classifier,
        X_test=X_test,
        y_test=y_test,
    )

    # ------------------------------------------------------------------- #
    # Save model artifacts
    LOGGER.info('Saving retraining artifacts')
    joblib.dump(
        classifier,
        f'{ARTIFACTS_DIR_PATH}/model.pkl',
    )
    joblib.dump(
        one_hot_encoder,
        f'{ARTIFACTS_DIR_PATH}/one_hot_encoder.pkl',
    )
    joblib.dump(
        ordinal_encoder,
        f'{ARTIFACTS_DIR_PATH}/ordinal_encoder.pkl',
    )

    # ------------------------------------------------------------------- #
    # Save retraining metrics
    retraining_metrics = {
        'split': {
            'train': 0.85,
            'test': 0.15,
        },
        'evaluation': {
            'train': [
                {
                    'metric_name': 'accuracy',
                    'metric_value': accuracy_train,
                },
            ],
            'test': [
                {
                    'metric_name': 'accuracy',
                    'metric_value': accuracy_test,
                },
            ],
        },
    }

    LOGGER.info('Saving retraining metrics')
    with open(METRICS_FILE_PATH, 'w') as file:
        json.dump(retraining_metrics, file)

    LOGGER.info('Retraining successfully completed')


if __name__ == '__main__':
    retrain()
