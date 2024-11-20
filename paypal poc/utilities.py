import json
import os

import boto3
import requests


def get_secret(secret_arn):
    """
    Get a secret from AWS Secrets Manager using the secret ARN.

    Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html

    Args:
        secret_arn: The ARN of the secret to get
    Returns:
        The secret string, usually a dictionary (e.g. {"vbrato/stripe/secret": "sk_test.....", "vbrato/stripe/key": "pk_test.....",})
    """

    region_name = os.environ["AWS_REGION"]

    session = boto3.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_arn)
    except Exception as e:
        raise e

    secret = json.loads(get_secret_value_response["SecretString"])
    return secret


PAYPAL_CLIENT_ID = get_secret("PayPalSecret")["vbrato/paypal/clientid"]
PAYPAL_SECRET = get_secret("PayPalSecret")["vbrato/paypal/secret"]
PAYPAL_API_BASE = (
    "https://api-m.sandbox.paypal.com"  # ToDo: Move to environment variable
)


def get_paypal_access_token():
    """Retrieve PayPal OAuth access token"""
    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )
    response.raise_for_status()
    return response.json()["access_token"]
