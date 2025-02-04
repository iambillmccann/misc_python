import stripe
import env

# Set your Stripe API key (ensure you're in test mode)
stripe.api_key = env.STRIPE_SECRET_KEY

try:
    # Create a token using the test card number that deposits funds immediately.
    token_response = stripe.Token.create(
        card={
            "number": "4000000000000077",  # Test card for available balance
            "exp_month": 12,
            "exp_year": 2026,
            "cvc": "123",
        }
    )

    print(f"Token created: {token_response.id}")

    # Create a test charge to add funds to your account
    charge = stripe.Charge.create(
        amount=500000,  # amount in cents, e.g., $500.00
        currency="usd",
        # source="tok_visa",  # Use Stripe's test token
        source=token_response.id,  # Use the token ID from the previous step
        description="Test charge to add funds to company account",
    )
except Exception as e:
    print(f"Failed to create charge: {e}")
    raise e

print(f"Test charge created: {charge.id}")
