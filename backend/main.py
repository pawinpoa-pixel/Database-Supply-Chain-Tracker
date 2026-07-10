from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, run_migrations
from routes import auth as auth_router
from routes.catalog import categories_router, products_router
from routes.partners import suppliers_router, customers_router, carriers_router
from routes.warehouses import warehouses_router, inventory_router
from routes.purchase_orders import router as purchase_orders_router
from routes.orders import router as orders_router
from routes.shipments import router as shipments_router
from routes.inventory_logs import router as inventory_logs_router
import models  # noqa: F401 - ensures all models are registered on Base before create_all

Base.metadata.create_all(bind=engine)
run_migrations()

app = FastAPI(title="Supply Chain Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(suppliers_router)
app.include_router(customers_router)
app.include_router(carriers_router)
app.include_router(warehouses_router)
app.include_router(inventory_router)
app.include_router(purchase_orders_router)
app.include_router(orders_router)
app.include_router(shipments_router)
app.include_router(inventory_logs_router)


@app.get("/")
def root():
    return {"status": "API is running"}
