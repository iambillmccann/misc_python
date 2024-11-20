import requests
import utilities

# PayPal API Base URL (set for sandbox)
PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"


def create_paypal_account_referral(email):
    """
    Create a PayPal account referral for a user.
    Args:
        email (str): The user's email address.
    Returns:
        dict: The referral link and metadata.
    """
    # Generate an access token
    access_token = utilities.get_paypal_access_token()

    # Referral request payload
    referral_payload = {
        "tracking_id": f"user-{email}",  # Track the user in your system
        "operations": [
            {
                "operation": "API_INTEGRATION",
                "api_integration_preference": {
                    "rest_api_integration": {
                        "integration_method": "PAYPAL",
                        "integration_type": "THIRD_PARTY",
                    }
                },
            }
        ],
        "products": ["EXPRESS_CHECKOUT"],  # The PayPal product for the user
        "legal_consents": [
            {
                "type": "SHARE_DATA_CONSENT",
                "granted": True,  # User consents to data sharing
            }
        ],
    }

    # Make the API request
    url = f"{PAYPAL_API_BASE}/v2/customer/partner-referrals"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=referral_payload)
    response.raise_for_status()

    # Extract and return referral data
    referral_data = response.json()
    return {
        "referral_link": referral_data["links"][1]["href"],  # The referral URL
        "tracking_id": referral_payload["tracking_id"],
        "email": email,
    }


# Example Usage
if __name__ == "__main__":
    try:
        # Set user details
        user_email = "testuser@example.com"

        # Generate a referral link
        referral_info = create_paypal_account_referral(user_email)
        print(f"Referral Link: {referral_info['referral_link']}")
        print(f"Tracking ID: {referral_info['tracking_id']}")
        print(f"User Email: {referral_info['email']}")
    except Exception as e:
        print(f"Failed to create referral link: {e}")
