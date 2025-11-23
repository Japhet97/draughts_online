from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Transaction, TransactionType
from app.schemas.schemas import DepositRequest, WithdrawalRequest, TransactionResponse, PaymentCallback
from app.api.endpoints.auth import get_current_user
from app.services.payment_service import paychangu_service
from typing import List
import uuid

router = APIRouter()


@router.post("/deposit")
async def initiate_deposit(
    deposit_data: DepositRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initiate a deposit transaction."""
    if not current_user.phone_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is required for deposits"
        )
    
    # Generate unique reference
    reference = f"DEP_{current_user.id}_{uuid.uuid4().hex[:12].upper()}"
    
    # Create pending transaction
    transaction = Transaction(
        user_id=current_user.id,
        type=TransactionType.DEPOSIT,
        amount=deposit_data.amount,
        balance_before=current_user.balance,
        payment_reference=reference,
        payment_method=deposit_data.payment_method,
        payment_status="pending",
        description=f"Deposit of {deposit_data.amount}"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Initiate payment with PayChangu
    result = await paychangu_service.initiate_deposit(
        user_id=current_user.id,
        amount=deposit_data.amount,
        phone_number=current_user.phone_number,
        reference=reference
    )
    
    if not result.get("success"):
        transaction.payment_status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment initiation failed: {result.get('error')}"
        )
    
    return {
        "message": "Deposit initiated. Please check your phone for payment prompt.",
        "transaction_id": transaction.id,
        "reference": reference,
        "amount": deposit_data.amount
    }


@router.post("/withdraw")
async def initiate_withdrawal(
    withdrawal_data: WithdrawalRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initiate a withdrawal transaction."""
    if not current_user.phone_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number is required for withdrawals"
        )
    
    if current_user.balance < withdrawal_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Generate unique reference
    reference = f"WTH_{current_user.id}_{uuid.uuid4().hex[:12].upper()}"
    
    # Deduct from balance immediately
    current_user.balance -= withdrawal_data.amount
    
    # Create pending transaction
    transaction = Transaction(
        user_id=current_user.id,
        type=TransactionType.WITHDRAWAL,
        amount=withdrawal_data.amount,
        balance_before=current_user.balance + withdrawal_data.amount,
        balance_after=current_user.balance,
        payment_reference=reference,
        payment_method=withdrawal_data.withdrawal_method,
        payment_status="pending",
        description=f"Withdrawal of {withdrawal_data.amount}"
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Initiate payout with PayChangu
    result = await paychangu_service.initiate_withdrawal(
        user_id=current_user.id,
        amount=withdrawal_data.amount,
        phone_number=current_user.phone_number,
        reference=reference
    )
    
    if not result.get("success"):
        # Refund user
        current_user.balance += withdrawal_data.amount
        transaction.payment_status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Withdrawal initiation failed: {result.get('error')}"
        )
    
    return {
        "message": "Withdrawal initiated. Funds will be sent to your mobile money account.",
        "transaction_id": transaction.id,
        "reference": reference,
        "amount": withdrawal_data.amount
    }


@router.post("/callback")
async def payment_callback(
    callback_data: PaymentCallback,
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle payment gateway callbacks."""
    # Verify signature (if provided in headers)
    signature = request.headers.get("X-PayChangu-Signature")
    if signature:
        if not paychangu_service.verify_callback_signature(callback_data.dict(), signature):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid signature"
            )
    
    # Find transaction
    transaction = db.query(Transaction).filter(
        Transaction.payment_reference == callback_data.reference
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Update transaction status
    transaction.payment_status = callback_data.status
    
    if callback_data.status == "success" or callback_data.status == "completed":
        if transaction.type == TransactionType.DEPOSIT:
            # Credit user account
            user = db.query(User).filter(User.id == transaction.user_id).first()
            user.balance += transaction.amount
            user.total_deposited += transaction.amount
            transaction.balance_after = user.balance
    elif callback_data.status == "failed":
        if transaction.type == TransactionType.WITHDRAWAL:
            # Refund user if withdrawal failed
            user = db.query(User).filter(User.id == transaction.user_id).first()
            user.balance += transaction.amount
    
    db.commit()
    
    return {"message": "Callback processed successfully"}


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's transaction history."""
    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(Transaction.created_at.desc()).limit(limit).all()
    
    return transactions


@router.get("/balance")
def get_balance(current_user: User = Depends(get_current_user)):
    """Get user's current balance."""
    return {
        "balance": current_user.balance,
        "total_deposited": current_user.total_deposited,
        "total_withdrawn": current_user.total_withdrawn
    }


@router.post("/test-complete/{transaction_id}")
async def complete_test_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Complete a test transaction (only works with test credentials)."""
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    if transaction.payment_status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Transaction already {transaction.payment_status}"
        )
    
    # Complete the transaction
    transaction.payment_status = "completed"
    
    if transaction.type == TransactionType.DEPOSIT:
        current_user.balance += transaction.amount
        current_user.total_deposited += transaction.amount
        transaction.balance_after = current_user.balance
    
    db.commit()
    
    return {
        "message": "Test transaction completed successfully",
        "transaction_id": transaction_id,
        "new_balance": current_user.balance
    }

