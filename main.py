from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import os

app = FastAPI()
PORT = int(os.environ.get("PORT", 10000))  # Critical for Render

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        output = remove(image_data)
        return StreamingResponse(io.BytesIO(output), media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health_check():
    return {"status": "active", "port": PORT}
