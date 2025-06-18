from banking_agents.dspy_agent.banking_agent import BankingAgent as DSPyBankingAgent
from banking_agents.smol_agent.banking_agent import BankingAgent as SmolBankingAgent
from banking_agents.autogen_agent.banking_agent import BankingAgent as AutoGenBankingAgent

def main():
    # Initialize all three agents
    dspy_agent = DSPyBankingAgent()
    smol_agent = SmolBankingAgent()
    autogen_agent = AutoGenBankingAgent()

    # Example queries to test
    queries = [
        "What's my current balance in account ACC001?",
        "Show me the last 3 transactions for my savings account",
        "Transfer $500 from my checking account to my savings account",
        "What are the details of account ACC003?",
        "How much money do I have in total across all my accounts?"
    ]

    # Test each agent with the queries
    print("\n=== DSPy Banking Agent ===")
    for query in queries:
        print(f"\nQuery: {query}")
        print(f"Response: {dspy_agent(query)}")

    print("\n=== SmolAgents Banking Agent ===")
    for query in queries:
        print(f"\nQuery: {query}")
        print(f"Response: {smol_agent.process_query(query)}")

    print("\n=== AutoGen Banking Agent ===")
    for query in queries:
        print(f"\nQuery: {query}")
        print(f"Response: {autogen_agent.process_query(query)}")

if __name__ == "__main__":
    main() 