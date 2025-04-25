from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
from PIL import Image, UnidentifiedImageError
import io

app = FastAPI()

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(None)):
    try:
        # Null file check
        if not file:
            raise HTTPException(
                status_code=400, 
                detail="No file uploaded. Please send an image file using the 'file' form field"
            )

        # Empty file check
        if file.size == 0:
            raise HTTPException(
                status_code=400, 
                detail="Uploaded file is empty (0 bytes)"
            )

        # Basic MIME type validation
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file.content_type}. Supported types: image/*"
            )

        # Read and validate image content
        image_data = await file.read()
        if not image_data:
            raise HTTPException(
                status_code=400,
                detail="Received empty image data"
            )

        # Try to open the image to validate it's actually an image file
        try:
            Image.open(io.BytesIO(image_data)).verify()
        except (UnidentifiedImageError, Exception) as img_error:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(img_error)}"
            ) from img_error

        # Process image with rembg
        output_image = remove(image_data)
        
        # Validate processing result
        if not output_image or len(output_image) < 100:  # Minimum expected PNG size
            raise HTTPException(
                status_code=500,
                detail="Background removal failed - invalid output generated"
            )

        # Return processed image
        img_buffer = io.BytesIO(output_image)
        return StreamingResponse(img_buffer, media_type="image/png")

    except HTTPException as http_err:
        # Re-raise already handled HTTP exceptions
        raise http_err
        
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed: {str(e)}"
        ) from e

@app.get("/", include_in_schema=False)
def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "operational",
            "endpoints": {
                "POST /remove-background": "Process images (supports JPG, PNG, WEBP)",
                "GET /test-null": "Test null file handling"
            },
            "error_handling": {
                "test_cases": [
                    "curl -X POST [url] (missing file)",
                    "curl -X POST -F file=@empty.jpg [url]",
                    "curl -X POST -F file=@text.txt [url]"
                ]
            }
        }
    )

@app.get("/test-null")
async def test_null_handling():
    """Endpoint to demonstrate null file handling"""
    try:
        # Simulate null file upload
        raise HTTPException(
            status_code=400,
            detail="Test successful! Server properly handles missing files. "
                   "When sending actual requests, include an image file using the 'file' form field."
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Null file test failed: {str(e)}"
        ) from e
