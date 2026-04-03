import os
from dotenv import load_dotenv
from twelvelabs import TwelveLabs

load_dotenv()

api_key = os.getenv("TWELVE_LABS_API_KEY")
if not api_key or api_key == "your_api_key_here":
    raise ValueError("Set TWELVE_LABS_API_KEY in your .env file")

client = TwelveLabs(api_key=api_key)

# List existing indexes
indexes = client.indexes.list()
print("Existing indexes:")
for index in indexes:
    print(f"  - {index.index_name} ({index.id})")
