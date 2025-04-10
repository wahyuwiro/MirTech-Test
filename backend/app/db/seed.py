from faker import Faker
from .models import Product, User, Order, Transaction, Base
from .database import engine, SessionLocal
import random
import datetime

fake = Faker()

def seed_data():
    db = SessionLocal()

    # Seed Products
    print("📦 Seeding products...")
    products = []
    for _ in range(100_000):
        product = Product(
            name=f"{fake.word().capitalize()}-{fake.uuid4()[:8]}",
            description=fake.text(max_nb_chars=100),
            price=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
            category=fake.word()
        )
        products.append(product)
    db.bulk_save_objects(products)
    db.commit()

    # Seed Users
    print("👤 Seeding users...")
    users = []
    for _ in range(1_000):
        user = User(
            name=fake.name(),
            email=fake.unique.email()
        )
        users.append(user)
    db.bulk_save_objects(users)
    db.commit()

    # Fetch IDs for referencing
    product_ids = [p.id for p in db.query(Product.id).all()]
    user_ids = [u.id for u in db.query(User.id).all()]

    # Seed Orders
    print("📑 Seeding orders...")
    orders = []
    for _ in range(10_000):
        order = Order(
            user_id=random.choice(user_ids),
            created_at=fake.date_time_this_year()
        )
        orders.append(order)
    db.bulk_save_objects(orders)
    db.commit()

    order_ids = [o.id for o in db.query(Order.id).all()]

    # Seed Transactions
    print("💸 Seeding transactions...")
    transactions = []
    for _ in range(50_000):
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 5)
        product = db.query(Product).filter(Product.id == product_id).first()
        total_price = round(product.price * quantity, 2)

        transaction = Transaction(
            order_id=random.choice(order_ids),
            product_id=product_id,
            quantity=quantity,
            total_price=total_price
        )
        transactions.append(transaction)
    
    db.bulk_save_objects(transactions)
    db.commit()
    db.close()

    print("✅ Done seeding all data!")

