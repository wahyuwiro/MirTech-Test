from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from app.db import models, database
from app import schemas
from app.cache import redis
import json
import hashlib
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
router = APIRouter()

# -- Products --
# @router.get("/products", response_model=list[schemas.ProductListResponse])
@router.get("/products", response_model=schemas.ProductListResponse)
def get_products(
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    search: str | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    db: Session = Depends(database.get_db)
):
    query_key = f"{category}-{search}-{sort_by}-{sort_order}-{skip}-{limit}"
    cache_key = f"products:{hashlib.md5(query_key.encode()).hexdigest()}"

    cached = redis.get_cached(cache_key)
    if cached:
        logger.info(f"✅ Cache HIT: {cache_key}")
        return json.loads(cached)

    logger.info(f"🚫 Cache MISS: {cache_key}")

    query = db.query(models.Product)

    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(models.Product.name.ilike(f"%{search}%"))

    if sort_by in ["name", "price", "id"]:
        sort_column = getattr(models.Product, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    total = query.count()
    products = query.offset(skip).limit(limit).all()

    serialized = [
        schemas.Product(
            id=p.id,
            name=p.name,
            description=p.description,
            price=p.price,
            category=p.category
        ) for p in products
    ]

    response_data = schemas.ProductListResponse(items=serialized, total=total)
    redis.set_cached(cache_key, response_data.json(), ttl=60)

    return response_data

# -- Users --
@router.get("/users", response_model=list[schemas.User])
def get_users(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    sort_by: str = "id",  # "name", "email"
    sort_order: str = "asc",  # "desc"
    db: Session = Depends(database.get_db)
):
    query_key = f"{search}-{sort_by}-{sort_order}-{skip}-{limit}"
    cache_key = f"users:{hashlib.md5(query_key.encode()).hexdigest()}"

    cached = redis.get_cached(cache_key)
    if cached:
        logger.info(f"✅ Cache HIT: {cache_key}")
        return json.loads(cached)

    logger.info(f"🚫 Cache MISS: {cache_key}")

    query = db.query(models.User)

    # Filtering
    if search:
        query = query.filter(models.User.name.ilike(f"%{search}%"))

    # Sorting
    if sort_by in ["name", "email", "id"]:
        sort_column = getattr(models.User, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    # Pagination
    users = query.offset(skip).limit(limit).all()

    # Serialize response
    serialized = [
        {
            "id": u.id,
            "name": u.name,
            "email": u.email
        } for u in users
    ]

    redis.set_cached(cache_key, json.dumps(serialized), ttl=60)
    return serialized

@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -- Orders --
@router.get("/orders", response_model=list[schemas.OrderWithUsername])
def get_orders(
    skip: int = 0,
    limit: int = 10,
    username: str | None = None,
    start_date: str | None = Query(None, example="2024-01-01"),
    end_date: str | None = Query(None, example="2025-01-01"),
    sort_by: str = "id",  # or "created_at"
    sort_order: str = "asc",  # or "desc"
    db: Session = Depends(database.get_db)
):
    # Create cache key from query params
    query_key = f"{username}-{start_date}-{end_date}-{sort_by}-{sort_order}-{skip}-{limit}"
    cache_key = f"orders:{hashlib.md5(query_key.encode()).hexdigest()}"

    cached = redis.get_cached(cache_key)
    if cached:
        logger.info(f"✅ Cache HIT: {cache_key}")
        return json.loads(cached)

    logger.info(f"🚫 Cache MISS: {cache_key}")

    # Build query
    query = db.query(models.Order).options(joinedload(models.Order.user))

    if username:
        query = query.join(models.User).filter(models.User.name.ilike(f"%{username}%"))

    # Parse and extend dates
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)

        query = query.filter(models.Order.created_at.between(start_dt, end_dt))

    # Apply sorting
    if sort_by in ["id", "created_at"]:
        sort_column = getattr(models.Order, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    # Pagination
    query = query.offset(skip).limit(limit)
    orders = query.all()

    # Serialize results
    serialized = [
        {
            "id": o.id,
            "user_id": o.user_id,
            "username": o.user.name if o.user else None,
            "created_at": o.created_at.isoformat()
        } for o in orders
    ]

    # Set cache
    redis.set_cached(cache_key, json.dumps(serialized), ttl=60)

    return serialized


@router.post("/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/orders/{order_id}")
def get_order_by_id(order_id: int, db: Session = Depends(database.get_db)):
    order = (
        db.query(models.Order)
        .options(
            joinedload(models.Order.user),
            joinedload(models.Order.transactions).joinedload(models.Transaction.product)  # Add product
        )
        .filter(models.Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "id": order.id,
        "user_id": order.user_id,
        "username": order.user.name if order.user else None,
        "created_at": order.created_at.isoformat(),
        "transactions": [
            {
                "id": tx.id,
                "quantity": tx.quantity,
                "total_price": tx.total_price,
                "product_id": tx.product_id,
                "product_name": tx.product.name if tx.product else None  # Add this line
            }
            for tx in order.transactions
        ]
    }


# -- Transactions --
@router.get("/transactions", response_model=list[schemas.Transaction])
def get_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return db.query(models.Transaction).offset(skip).limit(limit).all()

@router.post("/transactions", response_model=schemas.Transaction)
def create_transaction(tx: schemas.TransactionCreate, db: Session = Depends(database.get_db)):
    db_tx = models.Transaction(**tx.dict())
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx
