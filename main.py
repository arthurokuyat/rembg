import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
import io
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Send a POST request to /remove-bg with an image."}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents)).convert("RGBA")
    output_image = remove(input_image)

    buf = io.BytesIO()
    output_image.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use Render's PORT or default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
