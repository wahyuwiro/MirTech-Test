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

# -- Orders --
@router.get("/", response_model=schemas.OrderListResponse)
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


    logger.info(f"query : {query}")
    # Apply sorting
    if sort_by in ["id", "created_at"]:
        sort_column = getattr(models.Order, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    total = query.count()
    # Pagination
    query = query.offset(skip).limit(limit)
    orders = query.all()

    serialized = [
        schemas.Order(
            id= o.id,
            user_id= o.user_id,
            username= o.user.name if o.user else None,
            created_at= o.created_at.isoformat()
        ) for o in orders
    ]

    response_data = schemas.OrderListResponse(items=serialized, total=total)
    redis.set_cached(cache_key, response_data.json(), ttl=60)

    return response_data

    # # Serialize results
    # serialized = [
    #     {
    #         "id": o.id,
    #         "user_id": o.user_id,
    #         "username": o.user.name if o.user else None,
    #         "created_at": o.created_at.isoformat()
    #     } for o in orders
    # ]

    # # Set cache
    # redis.set_cached(cache_key, json.dumps(serialized), ttl=60)

    # return serialized


@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/{order_id}")
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
                "product_name": tx.product.name if tx.product else None,  # Add this line
                "product_price": tx.product.price if tx.product else None  # Add this line
            }
            for tx in order.transactions
        ]
    }