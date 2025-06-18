import dspy
from typing import List, Dict, Any
from agent_framework.database.dummy_transactions import (
    generate_dummy_transactions,
    get_account_balance,
    get_account_details,
    get_all_accounts,
    simulate_transfer
)

class BankingSignature(dspy.Signature):
    """Base signature for banking operations."""
    query: str = dspy.InputField(desc="The user's banking query")
    response: str = dspy.OutputField(desc="The response to the banking query")

class BalanceCheck(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = BankingSignature

    def forward(self, query: str) -> str:
        # Extract account ID from query
        account_id = "ACC001"  # Default
        if "savings" in query.lower():
            account_id = "ACC002"
        elif "jane" in query.lower():
            account_id = "ACC003"
        
        balance = get_account_balance(account_id)
        return f"Current balance for account {account_id}: ${balance:.2f}"

class TransactionHistory(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = BankingSignature

    def forward(self, query: str) -> str:
        # Extract account ID and number of transactions
        account_id = "ACC001"  # Default
        num_transactions = 5
        
        if "savings" in query.lower():
            account_id = "ACC002"
        elif "jane" in query.lower():
            account_id = "ACC003"
        
        transactions = generate_dummy_transactions(account_id, num_transactions)
        return f"Transaction history for account {account_id}:\n" + "\n".join(
            f"- {t['date']}: {t['type']} of ${abs(t['amount']):.2f} at {t['merchant']}"
            for t in transactions
        )

class Transfer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = BankingSignature

    def forward(self, query: str) -> str:
        # Extract transfer details
        from_account = "ACC001"
        to_account = "ACC002"
        amount = 100.0
        
        if "savings" in query.lower():
            to_account = "ACC002"
        if "checking" in query.lower():
            from_account = "ACC001"
        if "jane" in query.lower():
            if "from" in query.lower():
                from_account = "ACC003"
            else:
                to_account = "ACC003"
        
        result = simulate_transfer(from_account, to_account, amount)
        if result["status"] == "SUCCESS":
            return (
                f"Transfer successful!\n"
                f"From {from_account}: ${result['from_balance']:.2f}\n"
                f"To {to_account}: ${result['to_balance']:.2f}"
            )
        return f"Transfer failed: {result['message']}"

class AccountDetails(dspy.Module):
    def __init__(self):
        super().__init__()
        self.signature = BankingSignature

    def forward(self, query: str) -> str:
        # Extract account ID
        account_id = "ACC001"  # Default
        if "savings" in query.lower():
            account_id = "ACC002"
        elif "jane" in query.lower():
            account_id = "ACC003"
        
        details = get_account_details(account_id)
        if not details:
            return f"Account {account_id} not found"
        return f"Account Details for {account_id}:\n" + "\n".join(
            f"- {k}: {v}" for k, v in details.items()
        )

class BankingAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.balance_check = BalanceCheck()
        self.transaction_history = TransactionHistory()
        self.transfer = Transfer()
        self.account_details = AccountDetails()

    def forward(self, query: str) -> str:
        query = query.lower()
        
        if "balance" in query:
            return self.balance_check(query)
        elif "transaction" in query:
            return self.transaction_history(query)
        elif "transfer" in query:
            return self.transfer(query)
        elif "details" in query:
            return self.account_details(query)
        else:
            return "I'm not sure how to help with that. I can help with balance checks, transaction history, transfers, and account details." 