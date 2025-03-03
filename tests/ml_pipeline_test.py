import pytest
from unittest import mock
from app.train import load_data, preprocess_data, create_pipeline, train_model

# Test data loading
def test_load_data():
    url = "https://projet-cardiodetect.s3.eu-west-3.amazonaws.com/cardio_train.csv"
    df = load_data(url)
    assert not df.empty, "Dataframe is empty"

# Test data preprocessing
def test_preprocess_data():
    df = load_data("https://projet-cardiodetect.s3.eu-west-3.amazonaws.com/cardio_train.csv")
    X_train, X_test, y_train, y_test = preprocess_data(df)
    assert len(X_train) > 0, "Training data is empty"
    assert len(X_test) > 0, "Test data is empty"

# Test pipeline creation
def test_create_pipeline():
    pipe = create_pipeline()
    assert "standard_scaler" in pipe.named_steps, "Scaler missing in pipeline"
    assert "Random_Forest" in pipe.named_steps, "RandomForest missing in pipeline"

# Test model training (mocking GridSearchCV)
@mock.patch('app.train.GridSearchCV.fit', return_value=None)
def test_train_model(mock_fit):
    pipe = create_pipeline()
    X_train, X_test, y_train, y_test = preprocess_data(load_data("https://projet-cardiodetect.s3.eu-west-3.amazonaws.com/cardio_train.csv"))
    param_grid = {"Random_Forest__n_estimators": [90], "Random_Forest__criterion": ["squared_error"]}
    model = train_model(pipe, X_train, y_train, param_grid)
    assert model is not None, "Model training failed"
