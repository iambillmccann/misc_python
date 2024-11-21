import json
import boto3


def get_secret():
    """
    Get a secret from AWS Secrets Manager using the secret ARN.

    Docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html

    Args:
        secret_arn: The ARN of the secret to get
    Returns:
        The secret string, usually a dictionary (e.g. {"vbrato/stripe/secret": "sk_test.....", "vbrato/stripe/key": "pk_test.....",})
    """

    session = boto3.Session()
    client = session.client(service_name="secretsmanager", region_name="us-east-1")

    try:
        get_secret_value_response = client.get_secret_value(SecretId="PayPalSecret")
    except Exception as e:
        raise e

    secret = json.loads(get_secret_value_response["SecretString"])
    return secret
