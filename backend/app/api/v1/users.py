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

# -- Users --
@router.get("/", response_model=schemas.UserListResponse)
def get_users(
    skip: int = 0,
    limit: int = 10,
    search: str | None = None,
    email: str | None = None,
    sort_by: str = "id",  # "name", "email"
    sort_order: str = "asc",  # "desc"
    db: Session = Depends(database.get_db)
):
    query_key = f"{email}-{search}-{sort_by}-{sort_order}-{skip}-{limit}"
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

    if email:
        query = query.filter(models.User.email.ilike(f"%{email}%"))

    # Sorting
    if sort_by in ["name", "email", "id"]:
        sort_column = getattr(models.User, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
    
    total = query.count()    
    # Pagination
    users = query.offset(skip).limit(limit).all()

    serialized = [
        schemas.User(
            id= u.id,
            name= u.name,
            email= u.email,
        ) for u in users
    ]

    response_data = schemas.UserListResponse(items=serialized, total=total)
    redis.set_cached(cache_key, response_data.json(), ttl=60)

    return response_data

@router.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user