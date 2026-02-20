from langchain.tools import tool
from langchain_ollama import ChatOllama
from src.rag.data_loader import DataLoader
from src.rag.tools.pandas_tool import create_pandas_tool
from src.rag.tools.analysis_tool import create_analysis_tool
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

class FinancialAgent:
    def __init__(self, data_loader: DataLoader):
        self.llm = ChatOllama(model="llama3.1")

        self.tools = [create_pandas_tool(data_loader), create_analysis_tool(data_loader)]
        self.now = datetime.now()
        self.system_prompt = f"""You are a financial assistant helping users analyze their personal finances.

            Today's date: {self.now.strftime('%Y-%m-%d')} (year: {self.now.year}, month: {self.now.month}, day: {self.now.day}).
            Use this to resolve relative dates like "минулий місяць", "цей рік", etc.

            Available data:
            - expenses: year, month, category, amount
            - income: year, month, category, amount
            - savings: year, month, type, starting_balance, inflow, withdrawal, running_balance
            - currency_vault: year, month, opening_balance, salary_gross, converted, closing_balance

            Tools:
            - query_financial_data: For precise numerical queries (sums, comparisons, calculations)
            - analyze_finances: For analytical insights, advice, trend explanations

            Always respond in Ukrainian, even though this prompt is in English.
            Be concise and helpful.
            IMPORTANT: When a tool returns a result, include the EXACT returned value in your response.
            NEVER use placeholders like ${{result}}, {{result}}, or similar. Always use the actual data.
            Always respond in Ukrainian. Be concise and helpful.
            """
        self.agent = create_agent(model=self.llm, tools=self.tools, system_prompt=self.system_prompt)

    def query(self, question: str) -> str:
        result = self.agent.invoke({"messages": [{"role": "user", "content": question}]})
        return result["messages"][-1].content