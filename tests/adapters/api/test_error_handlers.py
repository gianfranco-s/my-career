"""Error handler response shape tests."""
import pytest
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel

from my_career.adapters.api.error_handlers import (
    unhandled_error_handler,
    validation_error_handler,
    value_error_handler,
)


class _Body(BaseModel):
    required_field: str


def _create_error_test_app() -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(ValueError, value_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)

    @app.post("/trigger-validation")
    def trigger_validation(body: _Body):
        return body

    @app.get("/trigger-value-error")
    def trigger_value_error():
        raise ValueError("something went wrong")

    @app.get("/trigger-unhandled")
    def trigger_unhandled():
        raise RuntimeError("unexpected")

    return app


@pytest.fixture(scope="module")
def error_client():
    return TestClient(_create_error_test_app(), raise_server_exceptions=False)


def test_validation_error_returns_422(error_client):
    response = error_client.post("/trigger-validation", json={})
    assert response.status_code == 422


def test_validation_error_response_shape(error_client):
    response = error_client.post("/trigger-validation", json={})
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert "message" in body["error"]


def test_value_error_returns_400(error_client):
    response = error_client.get("/trigger-value-error")
    assert response.status_code == 400


def test_value_error_response_shape(error_client):
    response = error_client.get("/trigger-value-error")
    body = response.json()
    assert body["error"]["code"] == "BAD_REQUEST"
    assert "something went wrong" in body["error"]["message"]


def test_unhandled_error_returns_500(error_client):
    response = error_client.get("/trigger-unhandled")
    assert response.status_code == 500


def test_unhandled_error_response_shape(error_client):
    response = error_client.get("/trigger-unhandled")
    body = response.json()
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert body["error"]["message"] == "An unexpected error occurred"
