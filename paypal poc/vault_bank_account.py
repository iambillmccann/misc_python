import requests
import json
import boto3

# from utilities import get_secret


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


def get_paypal_access_token():
    """Retrieve PayPal OAuth access token"""

    PAYPAL_CLIENT_ID = get_secret()["vbrato/paypal/clientid"]
    PAYPAL_SECRET = get_secret()["vbrato/paypal/secret"]
    PAYPAL_API_BASE = (
        "https://api-m.sandbox.paypal.com"  # ToDo: Move to environment variable
    )

    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        headers={"Accept": "application/json", "Accept-Language": "en_US"},
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


def vault_bank_account(account_details):
    """
    Vault a bank account using PayPal's Vault API.
    Args:
        account_details (dict): Bank account information to be vaulted.
            - account_number (str): The bank account number.
            - routing_number (str): The bank's routing number.
            - name (str): Name of the account holder.
            - account_type (str): Account type, e.g., "CHECKING" or "SAVINGS".
    Returns:
        dict: Vaulted bank account data, including the vault_id.
    """
    # Generate an access token
    access_token = get_paypal_access_token()

    # Vault request payload
    vault_payload = {
        "payment_source": {
            "bank": {
                "account_number": account_details["account_number"],
                "routing_number": account_details["routing_number"],
                "name": account_details["name"],
                "account_type": account_details.get("account_type", "CHECKING"),
                "currency": "USD",
            }
        }
    }

    # Make the API request
    url = f"{PAYPAL_API_BASE}/v2/vault/payment-methods"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=vault_payload)

    # Raise an exception if the request fails
    response.raise_for_status()

    # Return the vaulted bank account details
    return response.json()


# Main program logic
if __name__ == "__main__":
    try:
        # Simulated user bank account details
        user_bank_account = {
            "account_number": "123456789",  # Replace with a test account number
            "routing_number": "021000021",  # Replace with a test routing number
            "name": "John Doe",
            "account_type": "CHECKING",
        }

        # Vault the bank account
        vaulted_data = vault_bank_account(user_bank_account)
        print("Bank account vaulted successfully!")
        print(f"Vault ID: {vaulted_data['id']}")
        print(
            f"Masked Account Number: {vaulted_data['payment_source']['bank']['account_number']}"
        )
    except Exception as e:
        print(f"Failed to vault bank account: {e}")
