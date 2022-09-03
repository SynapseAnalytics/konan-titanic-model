from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

from utils.metrics import accuracy_score


def run_testing(
    classifier: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
):
    _y_pred_test = _predict(
        model=classifier,
        X=X_test,
    )
    _accuracy_test = accuracy_score(
        y_true=y_test,
        y_pred=_y_pred_test,
    )

    return _accuracy_test


def run_training(
    classifier_name: str,
    classifier: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
):
    print(datetime.now(), f'Starting to fit {classifier_name}')

    _fit_model = _train(
        classifier=classifier,
        X_train=X_train,
        y_train=y_train,
    )

    _ = _predict(
        model=_fit_model,
        X=X_train,
    )

    return _fit_model


def _train(
    classifier: Any,
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> Any:
    _fit_model = classifier.fit(
        np.array(X_train),
        np.array(y_train),
    )
    return _fit_model


def _predict(
    model: Any,
    X: pd.DataFrame,
) -> np.ndarray:
    _raw_output = model.predict(X)
    return _raw_output
