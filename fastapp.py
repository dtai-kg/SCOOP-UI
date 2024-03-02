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
from fastapi.staticfiles import StaticFiles
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
app.mount("/examples", StaticFiles(directory="static/examples"), name="examples")
app.mount("/images", StaticFiles(directory="static/images"), name="images")

@app.get("/")
async def index():
    # Return the index.html file
    return FileResponse("static/index.html", media_type="text/html")

class TranslationRequest(BaseModel):
    rmlData: str = None
    owlData: str = None
    xsdData: str = None


@app.post("/translate")
async def translate(request_data: TranslationRequest):

    try:
        # shutil.rmtree("temp_input")
        # os.mkdir("temp_input")
        # rml_file, owl_file, xsd_file = "temp_input/rml.ttl","temp_input/owl.txt","temp_input/xsd.xml"
        

        # shutil.rmtree("temp_output")
        # os.mkdir("temp_output")
        # output_file = "temp_output/shacl.ttl"

        
        os.mkdir("tmp")
        rml_file, owl_file, xsd_file, output_file= "tmp/rml.ttl","tmp/owl.txt","tmp/xsd.xml", "tmp/shacl.ttl"
        
        # temp_dir = tempfile.mkdtemp()
        # console.log("temp_dir",temp_dir)

        # rml_file = os.path.join(temp_dir, "rml.ttl")
        # owl_file = os.path.join(temp_dir, "owl.txt")
        # xsd_file = os.path.join(temp_dir, "xsd.xml")
        # output_file = os.path.join(temp_dir, "shacl.ttl")

        # shutil.rmtree(temp_dir)

        command = f"python scoop/main.py -ot {output_file}"

        mappings = request_data.rmlData
        if len(mappings)>5:
            rdflib.Graph().parse(data=mappings, format="turtle").serialize(
                destination=rml_file, format="turtle"
            )
            command += f" -m {rml_file} -xr {rml_file}"

        ontology = request_data.owlData
        if len(ontology)>5:
            open(owl_file, "w").write(ontology)
            command += f" -o {owl_file}"

        xsd = request_data.xsdData
        if len(xsd)>5:
            open(xsd_file, "w").write(xsd)
            command += f" -x {xsd_file}"

        result = subprocess.run(
            command, shell=True, capture_output=True, text=True
        )

        output = rdflib.Graph().parse(output_file, format="turtle").serialize(
            format="turtle"
        )

        shutil.rmtree("tmp")

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