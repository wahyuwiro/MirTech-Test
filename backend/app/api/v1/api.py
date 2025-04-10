from fastapi import APIRouter
from . import products, users, orders

router = APIRouter()

# Include individual route modules
router.include_router(products.router, prefix="/products", tags=["Products"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(orders.router, prefix="/orders", tags=["Orders"])
