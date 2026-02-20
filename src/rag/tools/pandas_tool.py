from langchain.tools import tool
from langchain_ollama import ChatOllama
import pandas as pd
from src.rag.data_loader import DataLoader
from src.config import Config

config = Config()


def _describe_df(name: str, df: pd.DataFrame, sample_rows: int = 3) -> str:
    return (
        f"DataFrame `{name}` — columns: {list(df.columns)}, "
        f"shape: {df.shape}\n"
        f"Sample:\n{df.head(sample_rows).to_string()}\n"
    )


def create_pandas_tool(dataloader: DataLoader):
    @tool
    def query_financial_data(question: str) -> str:
        """
        Use for precise numerical queries about expenses/income/savings/currency vault/monthlybudget/annual summary.
        Examples: amounts, comparisons, trends, calculations.

        Args:
            question (str): The question to ask about the expenses/income/savings/currency vault/monthlybudget/annual summary.

        Returns:
            The answer to the question.
        """

        dataframes = {
            "expenses_df": dataloader.get_expenses(),
            "income_df": dataloader.get_income(),
            "savings_df": dataloader.get_savings(),
            "currency_vault_df": dataloader.get_currency_vault(),
            "budget_df": dataloader.get_budget(),
            "summary_df": dataloader.get_summary(),
        }

        schema_description = "\n".join(
            _describe_df(name, df) for name, df in dataframes.items()
        )

        llm = ChatOllama(model="llama3.1", temperature=0)

        prompt = f"""You are a Python data analyst. Given the following pandas DataFrames, write a SHORT Python snippet that answers the user's question.

        AVAILABLE DATAFRAMES (already loaded as variables):
        {schema_description}

         - `expenses_df` columns: `year`, `month`, `category`, `amount`
            - `month` is a string like "January", "February" etc in English, not Ukrainian.
            - `category` is a string like "Продукти", "Кафе", "Техніка" etc in Ukrainian. Full list of categories is {config.Expenses_Categories}. Use `category` to filter when there is something about categoty in the question. For example, if the question is "Скільки я витратив на Продукти за Січень 2026?", you should use `category == "Продукти"` to filter the expenses_df to get the total amount of expenses on Products in January 2026.
            - `amount` is a float number in UAH.
            - `year` is a string like "2026", "2027" etc.
            - `description` is a string inUkrainian with comments to the transaction, but usually it's empty.
        - `income_df` columns: `year`, `month`, `category`, `amount`
            - `month` is a string like "January", "February" etc in English, not Ukrainian.
            - `category` is a string like "Оренда квартири", "A-Bank", "Продаж речей" etc in Ukrainian. Full list of categories is {config.Income_Categories}.
            - `amount` is a float number in UAH.
            - `year` is a string like "2026", "2027" etc.
            - `description` is a string in Ukrainian with comments to the transaction, but usually it's empty.
        - `savings_df` columns: `year`, `month`, `type`, `starting_balance`, `inflow`, `withdrawal`, `running_balance`
        - `currency_vault_df` columns: `year`, `month`, `opening_balance`, `salary_gross`, `converted`, `closing_balance`
        - `budget_df` columns: `year`, `month`, `opening_balance`, `total_income`, `total_expenses`, `transfer_to_savings`, `inflow_from_savings`, `net_cash_flow`, `closing_balance`
        - `summary_df` columns: `year`, `net_income`, `estimated_total_income_usd`, `total_lifestyle_expenses`, `avg_monthly_expenses`, `transfer_to_savings`, `inflow_from_savings`, `annual_cash_balance`

       RULES:
        - Use ONLY the provided DataFrames: {', '.join(dataframes.keys())}
        - Store the final answer in a variable called `result`.
        - Output ONLY valid Python code — no markdown, no explanations, no assigns, no print statements, no comments, no anything else.

        QUESTION: {question}
"""
        print('expenses_df:', dataframes['expenses_df'].head())

        response = llm.invoke(prompt)
        code = response.content.strip()

        code = code.removeprefix("```python").removeprefix("```").removesuffix("```").strip()
        print('generated code:',code)

        local_ns = {**dataframes, "pd": pd}
        try:
            exec(code, {"__builtins__": {}}, local_ns)
        except Exception as e:
            return f"Code execution error: {e}\nGenerated code:\n{code}"

        result = local_ns.get("result", "No `result` variable found in generated code.")
        print('result:', result)
        return str(result)

    return query_financial_data