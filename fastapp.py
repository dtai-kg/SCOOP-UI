from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import rdflib
import os
import shutil
import uvicorn
from fastapi.responses import FileResponse
from fastapi import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/")
async def index():
    return FileResponse("index.html", media_type="text/html", templates=True)

class TranslationRequest(BaseModel):
    rmlData: str = None
    owlData: str = None
    xsdData: str = None


@app.post("/translate")
async def translate(request_data: TranslationRequest):

    try:
        shutil.rmtree("temp_input")
        os.mkdir("temp_input")
        rml_file, owl_file, xsd_file = (
            "temp_input/rml.ttl",
            "temp_input/owl.txt",
            "temp_input/xsd.xml",
        )

        shutil.rmtree("temp_output")
        os.mkdir("temp_output")
        output_file = "temp_output/shacl.ttl"

        command = f"python scoop/main.py -ot {output_file}"

        mappings = request_data.rmlData
        if mappings:
            rdflib.Graph().parse(data=mappings, format="turtle").serialize(
                destination=rml_file, format="turtle"
            )
            command += f" -m {rml_file} -xr {rml_file}"

        ontology = request_data.owlData
        if ontology:
            open(owl_file, "w").write(ontology)
            command += f" -o {owl_file}"

        xsd = request_data.xsdData
        if xsd:
            open(xsd_file, "w").write(xsd)
            command += f" -x {xsd_file}"

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )

        output = rdflib.Graph().parse(output_file, format="turtle").serialize(
            format="turtle"
        )

        if result.returncode == 0:
            shacl_output = result.stdout
            response = JSONResponse(content={"shacl_output": output})
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response
        else:
            error_message = result.stderr
            return JSONResponse(content={"error": error_message}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)