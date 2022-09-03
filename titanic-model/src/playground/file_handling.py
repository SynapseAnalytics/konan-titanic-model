from typing import Any, Dict, Tuple
import yaml

from sklearn.model_selection import train_test_split
import pandas as pd


from data_preprocessing import preprocess_features, filter_features


def split_kaggle_data(
    source_directory: str = 'data/kaggle',
    write_directory: str = 'data/final',
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> None:
    dataset = pd.read_csv(f'{source_directory}/train.csv')
    dataset["survived"] = dataset["survived"].map({0: "no", 1: "yes"})
    
    features = dataset.drop('survived', axis=1)
    features = preprocess_features(features)
    features = filter_features(features)

    df = pd.concat([features, dataset['survived']], axis=1)

    remainder, test = train_test_split(
        df,
        test_size=test_ratio,
        random_state=42,
    )
    train, val = train_test_split(
        remainder,
        test_size=val_ratio,
        random_state=42,
    )

    train.to_csv(
        f'{write_directory}/train.csv',
        index=False,
    )
    val.to_csv(
        f'{write_directory}/val.csv',
        index=False,
    )
    test.to_csv(
        f'{write_directory}/test.csv',
        index=False,
    )


def read_data(
    directory: str = 'data/final',
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(f'{directory}/train.csv')
    val = pd.read_csv(f'{directory}/val.csv')

    return train, val


def read_metadata(
    directory: str = 'data',
) -> Dict[str, Any]:

    with open(f'{directory}/metadata.yml') as file:
        return yaml.safe_load(file)
