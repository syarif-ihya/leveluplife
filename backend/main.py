from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Izinkan akses dari frontend (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # bisa diganti nanti dengan domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is running"}

@app.get("/api/users")
def get_users():
    return [{"id": 1, "name": "Rin"}, {"id": 2, "name": "Adit"}]
