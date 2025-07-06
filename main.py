from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, product, supplier, incoming, outgoing
import uvicorn
import os

app = FastAPI()

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(supplier.router)
app.include_router(incoming.router)
app.include_router(outgoing.router)

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://textile-inventory.vercel.app", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"],             
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"--- Starting Uvicorn server on 0.0.0.0:{port} ---")
    uvicorn.run(app, host="0.0.0.0", port=port)