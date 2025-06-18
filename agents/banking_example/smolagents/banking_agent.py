from typing import List, Dict, Any, Callable
from agent_framework.database.dummy_transactions import (
    generate_dummy_transactions,
    get_account_balance,
    get_account_details,
    get_all_accounts,
    simulate_transfer
)

class BankingTool:
    """A simple banking tool implementation."""
    def __init__(self, name: str, description: str, function: Callable):
        self.name = name
        self.description = description
        self.function = function

def create_banking_tools() -> List[BankingTool]:
    """Create banking-specific tools."""
    return [
        BankingTool(
            name="check_balance",
            description="Check the balance of a bank account",
            function=lambda account_id: f"Current balance: ${get_account_balance(account_id):.2f}"
        ),
        BankingTool(
            name="get_transactions",
            description="Get transaction history for an account",
            function=lambda account_id, num=5: "\n".join(
                f"- {t['date']}: {t['type']} of ${abs(t['amount']):.2f} at {t['merchant']}"
                for t in generate_dummy_transactions(account_id, num)
            )
        ),
        BankingTool(
            name="transfer_money",
            description="Transfer money between accounts",
            function=lambda from_acc, to_acc, amount: (
                f"Transfer successful!\n"
                f"From {from_acc}: ${simulate_transfer(from_acc, to_acc, amount)['from_balance']:.2f}\n"
                f"To {to_acc}: ${simulate_transfer(from_acc, to_acc, amount)['to_balance']:.2f}"
            )
        ),
        BankingTool(
            name="get_account_details",
            description="Get detailed information about an account",
            function=lambda account_id: "\n".join(
                f"- {k}: {v}" for k, v in get_account_details(account_id).items()
            )
        )
    ]

class BankingAgent:
    def __init__(self):
        self.tools = create_banking_tools()
        self.system_prompt = """You are a helpful banking assistant. You can:
1. Check account balances
2. View transaction history
3. Transfer money between accounts
4. Get account details

Available accounts:
- ACC001 (Checking)
- ACC002 (Savings)
- ACC003 (Jane's Account)

Always format monetary values with dollar signs and two decimal places."""

    def process_query(self, query: str) -> str:
        """Process a banking query and return the response."""
        # Extract account information from query
        query = query.lower()
        account_id = "ACC001"  # Default
        
        if "savings" in query:
            account_id = "ACC002"
        elif "jane" in query:
            account_id = "ACC003"
        
        # Route query to appropriate tool
        if "balance" in query:
            tool = next(t for t in self.tools if t.name == "check_balance")
            return tool.function(account_id)
        elif "transaction" in query:
            tool = next(t for t in self.tools if t.name == "get_transactions")
            return tool.function(account_id)
        elif "transfer" in query:
            # Extract transfer details
            from_acc = "ACC001"
            to_acc = "ACC002"
            amount = 100.0
            
            if "savings" in query:
                to_acc = "ACC002"
            if "checking" in query:
                from_acc = "ACC001"
            if "jane" in query:
                if "from" in query:
                    from_acc = "ACC003"
                else:
                    to_acc = "ACC003"
            
            tool = next(t for t in self.tools if t.name == "transfer_money")
            return tool.function(from_acc, to_acc, amount)
        elif "details" in query:
            tool = next(t for t in self.tools if t.name == "get_account_details")
            return tool.function(account_id)
        else:
            return "I'm not sure how to help with that. I can help with balance checks, transaction history, transfers, and account details." 