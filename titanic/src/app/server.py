import joblib
import json
import pydantic
import yaml

import pandas as pd

from konan_sdk.konan_service.models import KonanServiceBaseModel
from konan_sdk.konan_service.services import KonanService
from konan_sdk.konan_service.serializers import (
    KonanServiceBasePredictionRequest, KonanServiceBasePredictionResponse,
    KonanServiceBaseEvaluateRequest, KonanServiceBaseEvaluateResponse
)

from titanic_enums import (
    Gender,
    EmbarkedPorts,
    TicketClass,
    Titles,
    SurvivedTypes,
)
from utils.encoding import (
    one_hot_encode,
    ordinal_encode,
)


ARTIFACTS_DIR = '/app/artifacts'


class MyPredictionRequest(KonanServiceBasePredictionRequest):
    """Defines the schema of a prediction request
    Follow the convention of <field_name>: <type_hint>
    Check https://pydantic-docs.helpmanual.io/usage/models/ for more info
    """
    pclass: TicketClass
    sex: Gender
    age: pydantic.NonNegativeInt
    sibsp: pydantic.NonNegativeInt = None
    parch: pydantic.NonNegativeInt = None
    fare: pydantic.NonNegativeFloat
    embarked: EmbarkedPorts = None
    title: Titles

    class Config:
        use_enum_values = True


class MyPredictionResponse(KonanServiceBasePredictionResponse):
    """Defines the schema of a prediction response
    Follow the convention of <field_name>: <type_hint>
    Check https://pydantic-docs.helpmanual.io/usage/models/ for more info
    """
    survived: SurvivedTypes


class MyModel(KonanServiceBaseModel):
    def __init__(self):
        """Add logic to initialize your actual model here

        Maybe load weights, connect to a database, etc ..
        """
        super().__init__()

        self.model = joblib.load(f'{ARTIFACTS_DIR}/model.pkl')
        self.one_hot_encoder = joblib.load(f'{ARTIFACTS_DIR}/one_hot_encoder.pkl')
        self.ordinal_encoder = joblib.load(f'{ARTIFACTS_DIR}/ordinal_encoder.pkl')

        self.metadata = yaml.safe_load(open(f'{ARTIFACTS_DIR}/metadata.yml'))

    def predict(self, req: MyPredictionRequest) -> MyPredictionResponse:
        """Makes an intelligent prediction

        Args:
            req (MyPredictionRequest): raw request from API

        Returns:
            MyPredictionResponse: this will be the response returned by the API
        """
        df = pd.DataFrame({k: [v] for k, v in json.loads(req.json()).items()})
        df, _ = one_hot_encode(
            df=df,
            columns=self.metadata['oneHotEncoding'],
            encoder=self.one_hot_encoder,
        )
        df, _ = ordinal_encode(
            df=df,
            columns=list(self.metadata['ordinalEncoding'].keys()),
            categories=list(self.metadata['ordinalEncoding'].values()),
            encoder=self.ordinal_encoder,
        )
        df = df.fillna(0)

        # Use your logic to make a prediction
        prediction = self.model.predict(df)
        print(prediction)

        # Create a MyPredictionResponse object using kwargs
        prediction_response = MyPredictionResponse(
            survived=SurvivedTypes.Yes if prediction else SurvivedTypes.No
        )

        # Optionally postprocess the prediction here
        return prediction_response

    def evaluate(self, req: KonanServiceBaseEvaluateRequest) -> KonanServiceBaseEvaluateResponse:
        """Evaluates the model based on passed predictions and their ground truths

        Args:
            req (KonanServiceBaseEvaluateRequest): includes passed predictions and their ground truths

        Returns:
            KonanServiceEvaluateResponse: the evaluation(s) of the model based on some metrics
        """
        raise NotImplementedError


app = KonanService(MyPredictionRequest, MyPredictionResponse, MyModel)
