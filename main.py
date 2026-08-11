from fastapi import FastAPI
app = FastAPI()
@app.get("/")
async def root():
    apiDictionary = {
        "name":"Task API",
        "version":"1.0",
        "endpoints":["/tasks"]
    }
    return apiDictionary
# health endpoint
@app.get("/health")
async def health():
    return{"status":"ok"}
