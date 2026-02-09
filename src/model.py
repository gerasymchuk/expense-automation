from pydantic import BaseModel

class TransactionRow(BaseModel):
    year: str
    month: str
    category: str
    amount: float
    description: str = ''

    def to_list(self) -> list:
        return [self.year, self.month, self.category, self.amount, self.description]