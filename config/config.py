from dotenv import load_dotenv
import os

load_dotenv()
token_asana = os.getenv("TOKEN")
URL_ASANA = "https://app.asana.com/api/1.0"
HEADERS_ASANA = {
    "Authorization": f"Bearer {token_asana}"
}
WORKSPACE_ASANA = os.getenv("WORKSPACE")
