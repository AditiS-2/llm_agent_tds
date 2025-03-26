from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import zipfile
import io

app = FastAPI()

@app.post("/api/")
async def answer_question(
    question: str = Form(...),
    file: UploadFile = None
):
    try:
        # Process file if provided
        if file:
            # Read the uploaded zip file
            zip_data = await file.read()
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data))
            
            # Extract CSV file inside the ZIP
            csv_filename = [name for name in zip_file.namelist() if name.endswith('.csv')][0]
            csv_file = zip_file.open(csv_filename)
            
            # Read CSV into a DataFrame
            df = pd.read_csv(csv_file)
            
            # Example: Extract value from "answer" column (adjust logic as needed)
            if "answer" in df.columns:
                answer_value = df["answer"].iloc[0]
                return JSONResponse(content={"answer": str(answer_value)})
            else:
                return JSONResponse(content={"error": "No 'answer' column found in the CSV."}, status_code=400)
        
        # Handle questions without files (custom logic can be added here)
        return JSONResponse(content={"answer": f"Processed question: {question}"})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
