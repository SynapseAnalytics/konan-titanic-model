import joblib
import json
import sys
import yaml
import os
import ast
import requests
from typing import Optional

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from utils.encoding import one_hot_encode, ordinal_encode
from utils.pipeline import run_testing, run_training

ARTIFACTS_DIR_PATH = '/app/artifacts'
METRICS_JSON_PATH = ast.literal_eval(os.getenv("METRICS_JSON_PATH"))
TRAINING_DATA_PATH = os.getenv("TRAINING_DATA_PATH")
SERVING_DATA_PATH = os.getenv("SERVING_DATA_PATH")


def retrain():
    # ------------------------------------------------------------------- #
    # Read the files
    print('Reading data files')
    training_data: Optional[pd.DataFrame] = None
    serving_data: Optional[pd.DataFrame] = None
    try:
        training_data = pd.read_csv(TRAINING_DATA_PATH)
        training_data['survived'].map({"yes": 1, "no": 0})
    except:
        pass
    try:
        serving_data = pd.read_csv(SERVING_DATA_PATH)
        # rename "ground_truth" to "survived"
        serving_data.rename(columns={'ground_truth': 'survived'}, inplace=True)
        serving_data['survived'].map({"yes": 1, "no": 0})
    except:
        pass

    if training_data is not None:
        print('Successfuly read training data %d rows and %d columns' % training_data.shape)
    if serving_data is not None:
        print('Successfuly read serving data %d rows and %d columns' % serving_data.shape)
    if training_data is None and serving_data is None:
        sys.exit('Unable to read both training and serving data')

    print('Finished reading data files')

    data = []
    if training_data is not None:
        data.append(training_data.reset_index(drop=True))
    if serving_data is not None:
        data.append(serving_data.reset_index(drop=True))

    # ------------------------------------------------------------------- #
    # Combine and split all data
    print('Preparing data for retraining')
    df = pd.concat(
        data,
        axis=0,
    )
    train, test = train_test_split(
        df,
        test_size=0.15,
        random_state=68,
    )

    print('Attempting to read required metadata file')
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

    print('Preprocessing the data')

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
    print('Beginning the retraining')
    classifier = run_training(
        classifier_name="knn",
        classifier=KNeighborsClassifier(
            n_neighbors=3,
        ),
        X_train=X_train,
        y_train=y_train,
    )
    print('Calculating metrics on training data')
    accuracy_train = run_testing(
        classifier=classifier,
        X_test=X_train,
        y_test=y_train,
    )
    print('Calculating metrics on testing data')
    accuracy_test = run_testing(
        classifier=classifier,
        X_test=X_test,
        y_test=y_test,
    )

    # ------------------------------------------------------------------- #
    # Save model artifacts
    print('Saving retraining artifacts')
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

    with open('metrics.json', 'w') as file:
        json.dump(retraining_metrics, file)

    print('Saving retraining metrics')
    with open('metrics.json', 'rb') as file:
        files = {'file': ('metrics.json', file)}
        _ = requests.post(METRICS_JSON_PATH['url'], data=METRICS_JSON_PATH['fields'], files=files)

    print('Retraining successfully completed')


if __name__ == '__main__':
    retrain()
