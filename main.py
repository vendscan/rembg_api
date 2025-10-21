from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-single")
async def remove_single(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = remove(image_bytes)

    output = BytesIO(result)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="image/png",
        headers={"Content-Disposition": 'attachment; filename="no_bg.png"'}
    )

@app.post("/remove-batch")
async def remove_batch(files: list[UploadFile] = File(...)):
    result_list = []

    for file in files:
        image_bytes = await file.read()
        result = remove(image_bytes)

        encoded = base64.b64encode(result).decode("utf-8")
        result_list.append(encoded)

    return JSONResponse(content={"images": result_list})
