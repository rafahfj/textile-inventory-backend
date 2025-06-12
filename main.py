from fastapi import FastAPI
from routers import auth, product, supplier, incoming, outgoing
import uvicorn
import os

app = FastAPI()

app.include_router(product.router)
app.include_router(auth.router)
app.include_router(supplier.router)
app.include_router(incoming.router)
app.include_router(outgoing.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"--- Starting Uvicorn server on 0.0.0.0:{port} ---") # Baris opsional untuk debugging
    uvicorn.run(app, host="0.0.0.0", port=port)