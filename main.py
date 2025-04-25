from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg import remove
import io
import os

app = FastAPI()

# Get port from Render's environment variable
PORT = int(os.environ.get("PORT", 10000))

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        output = remove(image_data)
        return StreamingResponse(io.BytesIO(output), media_type="image/png")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)  # Explicit port binding
