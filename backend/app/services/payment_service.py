import httpx
import hashlib
import json
from typing import Optional, Dict
from app.core.config import settings


class PayChanguService:
    """
    PayChangu payment gateway integration.
    Supports deposits and withdrawals for mobile money payments.
    """
    
    def __init__(self):
        self.api_key = settings.PAYCHANGU_API_KEY
        self.secret_key = settings.PAYCHANGU_SECRET_KEY
        self.base_url = settings.PAYCHANGU_BASE_URL
        self.callback_url = settings.PAYCHANGU_CALLBACK_URL
        self.test_mode = self.api_key.startswith("test_")  # Auto-detect test mode
    
    def generate_signature(self, data: dict) -> str:
        """Generate signature for PayChangu API request."""
        # Sort the data by keys
        sorted_data = dict(sorted(data.items()))
        # Create string to sign
        string_to_sign = json.dumps(sorted_data, separators=(',', ':'))
        # Add secret key
        string_to_sign += self.secret_key
        # Generate SHA256 hash
        signature = hashlib.sha256(string_to_sign.encode()).hexdigest()
        return signature
    
    async def initiate_deposit(
        self, 
        user_id: int, 
        amount: float, 
        phone_number: str,
        reference: str
    ) -> Dict:
        """
        Initiate a deposit transaction.
        
        Args:
            user_id: User ID making the deposit
            amount: Amount to deposit
            phone_number: User's phone number for mobile money
            reference: Unique transaction reference
        
        Returns:
            Dictionary with transaction details
        """
        # TEST MODE: Auto-approve without calling real API
        if self.test_mode:
            return {
                "success": True,
                "transaction_id": reference,
                "status": "pending",
                "message": "TEST MODE: Deposit initiated. Transaction will auto-complete in callback."
            }
        
        try:
            payload = {
                "api_key": self.api_key,
                "tx_ref": reference,
                "amount": amount,
                "currency": "MWK",  # Malawian Kwacha
                "phone_number": phone_number,
                "callback_url": self.callback_url,
                "transaction_metadata": {
                    "user_id": user_id,
                    "transaction_type": "deposit"
                }
            }
            
            # Generate signature
            payload["signature"] = self.generate_signature(payload)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/payments/mobile-money",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "transaction_id": result.get("transaction_id"),
                        "status": result.get("status"),
                        "message": result.get("message")
                    }
                else:
                    return {
                        "success": False,
                        "error": response.text
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def initiate_withdrawal(
        self, 
        user_id: int, 
        amount: float, 
        phone_number: str,
        reference: str
    ) -> Dict:
        """
        Initiate a withdrawal transaction.
        
        Args:
            user_id: User ID making the withdrawal
            amount: Amount to withdraw
            phone_number: User's phone number for mobile money
            reference: Unique transaction reference
        
        Returns:
            Dictionary with transaction details
        """
        # TEST MODE: Auto-approve without calling real API
        if self.test_mode:
            return {
                "success": True,
                "transaction_id": reference,
                "status": "pending",
                "message": "TEST MODE: Withdrawal initiated. Funds will be sent in test mode."
            }
        
        try:
            payload = {
                "api_key": self.api_key,
                "tx_ref": reference,
                "amount": amount,
                "currency": "MWK",
                "phone_number": phone_number,
                "callback_url": self.callback_url,
                "transaction_metadata": {
                    "user_id": user_id,
                    "transaction_type": "withdrawal"
                }
            }
            
            # Generate signature
            payload["signature"] = self.generate_signature(payload)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/payouts/mobile-money",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "transaction_id": result.get("transaction_id"),
                        "status": result.get("status"),
                        "message": result.get("message")
                    }
                else:
                    return {
                        "success": False,
                        "error": response.text
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def verify_transaction(self, transaction_id: str) -> Dict:
        """
        Verify a transaction status.
        
        Args:
            transaction_id: Transaction ID to verify
        
        Returns:
            Dictionary with transaction status
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/transactions/{transaction_id}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "success": False,
                        "error": response.text
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def verify_callback_signature(self, payload: dict, signature: str) -> bool:
        """
        Verify the signature from PayChangu callback.
        
        Args:
            payload: Callback payload
            signature: Signature to verify
        
        Returns:
            True if signature is valid, False otherwise
        """
        expected_signature = self.generate_signature(payload)
        return signature == expected_signature


# Create singleton instance
paychangu_service = PayChanguService()
