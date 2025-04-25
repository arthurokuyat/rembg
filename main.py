from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from rembg.bg import remove
from PIL import Image
import io
import os

app = FastAPI()

# Get port from Render's environment variable
PORT = int(os.environ.get("PORT", 10000))

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
        output_image = Image.fromarray(remove(input_image))

        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)  # Explicit port binding
