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
@router.get("/", response_model=schemas.ProductListResponse)
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


    logger.info(f"query : {query}")
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