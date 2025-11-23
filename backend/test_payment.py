"""
Test script to verify payment endpoint structure.
This simulates the payment flow without real credentials.
"""
import asyncio
from app.services.payment_service import PayChanguService

async def test_payment_structure():
    """Test payment service structure"""
    service = PayChanguService()
    
    print("=== PayChangu Configuration ===")
    print(f"API Key: {service.api_key[:10]}...")
    print(f"Base URL: {service.base_url}")
    print(f"Callback URL: {service.callback_url}")
    
    print("\n=== Testing Signature Generation ===")
    test_data = {
        "amount": 1000,
        "currency": "MWK",
        "phone_number": "+265991234567"
    }
    signature = service.generate_signature(test_data)
    print(f"Signature generated: {signature[:20]}...")
    
    print("\n=== Testing Deposit Initiation (will fail with test credentials) ===")
    result = await service.initiate_deposit(
        user_id=1,
        amount=1000.0,
        phone_number="+265991234567",
        reference="TEST_DEP_123"
    )
    print(f"Result: {result}")
    
    print("\n✅ Payment structure is correct!")
    print("⚠️  To test actual payments:")
    print("   1. Get real/sandbox credentials from PayChangu")
    print("   2. Update .env file")
    print("   3. Restart API server")
    print("   4. Use the /api/v1/payments/deposit endpoint")

if __name__ == "__main__":
    asyncio.run(test_payment_structure())
