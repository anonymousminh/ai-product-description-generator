import json
import pytest
from botocore.exceptions import ClientError

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

from product_generator.services.bedrock_service import BedrockService

# Fixture to mock the boto3 client for bedrock-runtime
@pytest.fixture
def mock_bedrock_runtime_client(mocker):
    mock_client = mocker.MagicMock()
    mocker.patch(
        'product_generator.services.bedrock_service.boto3.client',
        return_value=mock_client
    )
    return mock_client

# Fixture to create an instance of BedrockService for each test, after boto3 is patched
@pytest.fixture
def bedrock_service_instance(mock_bedrock_runtime_client):
    return BedrockService(region="us-east-2")

# Test successful invocation of a model
def test_invoke_model_success(bedrock_service_instance, mock_bedrock_runtime_client, mocker):
    # Configure the mock client's invoke_model method
    mock_response_body = {"generation": "This is a generated description."}
    mock_bedrock_runtime_client.invoke_model.return_value = {
        "body": mocker.MagicMock(read=lambda: json.dumps(mock_response_body).encode('utf-8'))
    }

    prompt = "Generate a description."
    response_text = bedrock_service_instance.invoke_model(prompt)

    assert response_text == "This is a generated description."
    mock_bedrock_runtime_client.invoke_model.assert_called_once()

    # Verify the arguments passed to invoke_model
    args, kwargs = mock_bedrock_runtime_client.invoke_model.call_args
    assert kwargs["modelId"] == "meta.llama3-3-70b-instruct-v1:0"

# Test handling of ClientError from boto3
def test_invoke_model_client_error(bedrock_service_instance, mock_bedrock_runtime_client, capsys):
    # Configure the mock client to raise a ClientError
    mock_bedrock_runtime_client.invoke_model.side_effect = ClientError(
        {"Error": {"Code": "ValidationException", "Message": "Invalid request"}},
        "InvokeModel"
    )

    prompt = "Generate a description."

    # Expect the function to exit and print an error message
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        bedrock_service_instance.invoke_model(prompt)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1 # Check the exit code

    # Capture stdout/stderr to check the printed error message
    captured = capsys.readouterr()
    assert "ERROR: Can't invoke 'meta.llama3-3-70b-instruct-v1:0'. Reason:" in captured.out

# Test handling of generic Exception
def test_invoke_model_generic_error(bedrock_service_instance, mock_bedrock_runtime_client, capsys):
    # Configure the mock client to raise a generic Exception
    mock_bedrock_runtime_client.invoke_model.side_effect = Exception("Something went wrong")

    prompt = "Generate a description."

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        bedrock_service_instance.invoke_model(prompt)

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

    captured = capsys.readouterr()
    assert "ERROR: Can't invoke 'meta.llama3-3-70b-instruct-v1:0'. Reason:" in captured.out

