import stripe
import env

# Set your Stripe API key (ensure you're in test mode)
stripe.api_key = env.STRIPE_SECRET_KEY

try:
    # Create a test charge to add funds to your account
    charge = stripe.Charge.create(
        amount=500000,  # amount in cents, e.g., $500.00
        currency="usd",
        source="tok_visa",  # Use Stripe's test token
        description="Test charge to add funds to company account",
    )
except Exception as e:
    print(f"Failed to create charge: {e}")
    raise e

print(f"Test charge created: {charge.id}")
