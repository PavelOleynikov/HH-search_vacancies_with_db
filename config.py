from dotenv import load_dotenv
import os


load_dotenv()

host = os.getenv("DATABASE_HOST")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
dbname = os.getenv("DATABASE_NAME")
