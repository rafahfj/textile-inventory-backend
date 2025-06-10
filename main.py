
from fastapi import FastAPI
from routers import product, user, supplier, incoming, outgoing
import uvicorn
import os

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from Railway!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080)) # Pastikan baris ini ada
    uvicorn.run(app, host="0.0.0.0", port=port)

app.include_router(product.router)
app.include_router(user.router)
app.include_router(supplier.router)
app.include_router(incoming.router)
app.include_router(outgoing.router)