
from fastapi import FastAPI
from routers import product, user, supplier, incoming, outgoing

app = FastAPI()
app.include_router(product.router)
app.include_router(user.router)
app.include_router(supplier.router)
app.include_router(incoming.router)
app.include_router(outgoing.router)