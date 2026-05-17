# services/payment_simulator.py
# Simulates payment processing for different payment methods.

VALID_PAYMENT_METHODS = ["Cash", "Mock Card", "Mock Card Fail"]

def process_payment(payment_method):
    """
    Simulates processing a payment.

    Returns:
        dict with "success": True on success,
        or "success": False and "error" message on failure.
    """

    # Check if payment_method is provided and valid
    if not payment_method or payment_method not in VALID_PAYMENT_METHODS:
        return {"success": False, "error": "Invalid payment method"}

    # Simulate a failed card payment
    if payment_method == "Mock Card Fail":
        return {"success": False, "error": "Payment failed. Please try again."}

    # Cash and Mock Card succeed
    return {"success": True}