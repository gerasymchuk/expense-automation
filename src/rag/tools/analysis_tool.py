from langchain.tools import tool
from langchain_ollama import ChatOllama
import pandas as pd
from src.rag.data_loader import DataLoader


def create_analysis_tool(dataloader: DataLoader) -> str:
    @tool
    def analyze_finances(question: str) -> str:
        """
        Use for analysis of the financial data: suggestions, recommendations, insights,financial habits, trends explanation, etc.

        Args:
            question (str): The question about any aspect of the financial data.

        Returns:
            The answer to the question.
        """

        expenses_df = dataloader.get_expenses().to_markdown(index=False)
        income_df = dataloader.get_income().to_markdown(index=False)
        savings_df = dataloader.get_savings().to_markdown(index=False)
        currency_vault_df = dataloader.get_currency_vault().to_markdown(index=False)
        budget_df = dataloader.get_budget().to_markdown(index=False)
        summary_df = dataloader.get_summary().to_markdown(index=False)

        llm = ChatOllama(
            model="llama3.1",
            temperature=0
        )
        prompt = f"""
        You are a financial analyst. You are given a question to analyze the financial data.
        You need to analyze the financial data and provide suggestions, recommendations, insights,financial habits, trends explanation, etc.
        The question is: {question}
        The expenses dataframe is: {expenses_df}
        The income dataframe is: {income_df}
        The savings dataframe is: {savings_df}
        The currency vault dataframe is: {currency_vault_df}
        The budget dataframe is: {budget_df}
        The summary (annual) dataframe is: {summary_df}
        """
        response = llm.invoke(prompt)
        return response.content

    return analyze_finances