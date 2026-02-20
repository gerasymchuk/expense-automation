from src.rag.data_loader import DataLoader
from src.rag.agent import FinancialAgent
from src.config import Config
from src.sheets_manager import SheetsManager
from src.rag.data_loader import CacheManager

def main():
    config = Config()
    config.validate()
    config.validate_csv(config.CSV_PATH)
    sheets_manager = SheetsManager(config.SHEET_ID, config.CREDENTIALS_PATH)
    cache = CacheManager(config.CACHE_DIR)
    data_loader = DataLoader(sheets_manager=sheets_manager, cache=cache)
    agent = FinancialAgent(data_loader)
    result = agent.query("Підкажи інсайти про витрати минулої осені")
    print(result)

if __name__ == "__main__":
    main()