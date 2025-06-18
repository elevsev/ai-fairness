import autogen
from typing import List, Dict, Any
from agent_framework.database.dummy_transactions import (
    generate_dummy_transactions,
    get_account_balance,
    get_account_details,
    get_all_accounts,
    simulate_transfer
)

def check_balance(account_id: str) -> str:
    """Check the balance of a bank account."""
    balance = get_account_balance(account_id)
    return f"Current balance for account {account_id}: ${balance:.2f}"

def get_transactions(account_id: str, num_transactions: int = 5) -> str:
    """Get transaction history for an account."""
    transactions = generate_dummy_transactions(account_id, num_transactions)
    return f"Transaction history for account {account_id}:\n" + "\n".join(
        f"- {t['date']}: {t['type']} of ${abs(t['amount']):.2f} at {t['merchant']}"
        for t in transactions
    )

def transfer_money(from_account: str, to_account: str, amount: float) -> str:
    """Transfer money between accounts."""
    result = simulate_transfer(from_account, to_account, amount)
    if result["status"] == "SUCCESS":
        return (
            f"Transfer successful!\n"
            f"From {from_account}: ${result['from_balance']:.2f}\n"
            f"To {to_account}: ${result['to_balance']:.2f}"
        )
    return f"Transfer failed: {result['message']}"

def get_account_info(account_id: str) -> str:
    """Get detailed information about an account."""
    details = get_account_details(account_id)
    if not details:
        return f"Account {account_id} not found"
    return f"Account Details for {account_id}:\n" + "\n".join(
        f"- {k}: {v}" for k, v in details.items()
    )

class MockLLM:
    """A mock LLM that returns predefined responses based on the query."""
    def __init__(self):
        self.responses = {
            "balance": "I'll check the balance for you.",
            "transaction": "I'll get the transaction history for you.",
            "transfer": "I'll help you transfer the money.",
            "details": "I'll get the account details for you.",
            "total": "I'll calculate the total balance across all accounts."
        }

    def generate(self, messages, *args, **kwargs):
        # Extract the last message
        last_message = messages[-1]["content"].lower()
        
        # Find the appropriate response
        response = "I'm not sure how to help with that."
        for key, value in self.responses.items():
            if key in last_message:
                response = value
                break
        
        return {"choices": [{"message": {"content": response}}]}

class BankingAgent:
    def __init__(self):
        # Create a mock LLM configuration
        mock_llm_config = {
            "config_list": [{"model": "mock-model"}],
            "cache_seed": None,
            "temperature": 0,
            "timeout": 60,
            "llm": MockLLM()
        }

        # Create the banking assistant agent
        self.banking_assistant = autogen.AssistantAgent(
            name="BankingAssistant",
            system_message="""You are a helpful banking assistant. You can:
1. Check account balances
2. View transaction history
3. Transfer money between accounts
4. Get account details

Available accounts:
- ACC001 (Checking)
- ACC002 (Savings)
- ACC003 (Jane's Account)

Always format monetary values with dollar signs and two decimal places.""",
            llm_config=mock_llm_config
        )

        # Create the user proxy agent with Docker disabled
        self.user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "banking_workspace",
                "use_docker": False
            },
            llm_config=mock_llm_config
        )

        # Register banking functions
        self.user_proxy.register_function(
            function_map={
                "check_balance": check_balance,
                "get_transactions": get_transactions,
                "transfer_money": transfer_money,
                "get_account_info": get_account_info
            }
        )

    def process_query(self, query: str) -> str:
        """Process a banking query and return the response."""
        # Extract account information from query
        query = query.lower()
        account_id = "ACC001"  # Default
        
        if "savings" in query:
            account_id = "ACC002"
        elif "jane" in query:
            account_id = "ACC003"
        
        # Route query to appropriate function
        if "balance" in query:
            return check_balance(account_id)
        elif "transaction" in query:
            return get_transactions(account_id)
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
            
            return transfer_money(from_acc, to_acc, amount)
        elif "details" in query:
            return get_account_info(account_id)
        else:
            return "I'm not sure how to help with that. I can help with balance checks, transaction history, transfers, and account details." 