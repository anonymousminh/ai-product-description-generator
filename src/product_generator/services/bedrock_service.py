import boto3
import json
from botocore.exceptions import ClientError

class BedrockService:
    def __init__(self, region="us-east-2"):
        # Create a Bedrock Runtime client in the specified AWS Region.
        self.client = boto3.client("bedrock-runtime", region_name=region)

    def invoke_model(self, prompt):
        # Set the model ID, e.g., Llama 3 70b Instruct.
        model_id = "meta.llama3-3-70b-instruct-v1:0"

        # Embed the prompt in Llama 3's instruction format.
        formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{prompt}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

        # Format the request payload using the model's native structure.
        native_request = {
            "prompt": formatted_prompt,
            "max_gen_len": 512,
            "temperature": 0.5,
        }

        # Convert the native request to JSON.
        request_payload = json.dumps(native_request)

        try:
            # Invoke the model with the request.
            response = self.client.invoke_model(modelId=model_id, body=request_payload)
        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
            exit(1)

        # Decode the response body.
        model_response = json.loads(response["body"].read())

        # Extract and print the response text.
        response_text = model_response.get("generation", "")
        return response_text