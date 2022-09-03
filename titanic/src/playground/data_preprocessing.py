import pandas as pd


def preprocess_features(
    features: pd.DataFrame,
) -> pd.DataFrame:
    """Engineer the Titanic dataset features according to https://www.kaggle.com/code/startupsci/titanic-data-science-solutions

    Args:
        features (pd.DataFrame): raw features

    Returns:
        pd.DataFrame: engineered features
    """
    _df = features.copy()

    # Construct Title feature from Name
    _df['title'] = _df['name'].str.extract(' ([A-Za-z]+)\\.', expand=False)
    _df['title'] = _df['title'].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
    _df['title'] = _df['title'].replace('Mlle', 'Miss')
    _df['title'] = _df['title'].replace('Ms', 'Miss')
    _df['title'] = _df['title'].replace('Mme', 'Mrs')

    return _df


def filter_features(
    df: pd.DataFrame,
):
    _df = df.copy().drop(
        columns=[
            'passenger_id',
            'name',
            'ticket',
            # 'fare',
            'boat',
            'body',
            'cabin',
            'home.dest',
        ],
    )

    return _df
