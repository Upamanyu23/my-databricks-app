from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "/Volumes/workspace/default/uploads"
OUTPUT_FOLDER = "/Volumes/workspace/default/output"

# create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.post("/convert")
async def convert_excel_to_csv(file: UploadFile = File(...)):

    # Save uploaded Excel file
    excel_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(excel_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read Excel file
    df = pd.read_excel(excel_path)

    # Create CSV filename
    csv_filename = file.filename.replace(".xlsx", ".csv")
    csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)

    # Save CSV
    df.to_csv(csv_path, index=False)

    return FileResponse(
        csv_path,
        media_type="text/csv",
        filename=csv_filename
    )
