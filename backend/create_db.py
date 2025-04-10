import time
from app.db.models import Base
from app.db.database import engine
from app.db.seed import seed_data

# Wait for DB to be ready
for i in range(5):
    try:
        print("🔧 Creating database schema...")
        Base.metadata.create_all(bind=engine)
        print("✅ Done!")
        break
    except Exception:
        print(f"Database not ready, retrying in 3s... ({i+1}/5)")
        time.sleep(3)

# Seed all data (products, users, orders, transactions)
seed_data()
