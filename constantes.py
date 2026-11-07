import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
import urllib.parse

load_dotenv()

API_KEY = os.getenv("API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    print(" Detectada configuração de NUVEM (Neon).")
    
    if DATABASE_URL.startswith("postgres://"):
        DB_STRING = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    else:
        DB_STRING = DATABASE_URL

else:
    print("💻 Nenhuma configuração de nuvem detectada. Tentando LOCAL.")
    
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    
    if not DB_PASS:
        raise RuntimeError(
            "DB_PASS não definido. Configure a senha do banco no arquivo .env."
        )

    DB_PASS_ENCODED = urllib.parse.quote_plus(DB_PASS)
    DB_STRING = f"postgresql://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

TICKER = "AAPL"
EMPRESA = "Apple Inc."

db_engine = None
try:
    db_engine = create_engine(DB_STRING, pool_pre_ping=True)
except Exception as e:
    print(f"❌ Erro ao criar a engine do banco de dados: {e}")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stockintel_pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)