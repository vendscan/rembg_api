from fastapi import FastAPI, UploadFile, File
from rembg import remove
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()

def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


@app.post("/remove-single")
async def remove_single_api(file: UploadFile = File(...)):
    img = Image.open(BytesIO(await file.read()))
    out = remove(img)

    base64_image = image_to_base64(out)
    return {"image_base64": base64_image}


@app.post("/remove-batch")
async def remove_batch_api(files: list[UploadFile] = File(...)):
    base64_images = []

    for file in files:
        img = Image.open(BytesIO(await file.read()))
        out = remove(img)
        base64_images.append(image_to_base64(out))

    return {"images": base64_images}
