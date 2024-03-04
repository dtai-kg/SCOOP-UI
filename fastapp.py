from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import rdflib
import os
import sys
import shutil
import uvicorn
from fastapi.responses import FileResponse
from fastapi import Response
from fastapi.staticfiles import StaticFiles
import tempfile
from rdflib import Graph
from pyshacl import validate
import multiprocessing as mp
from scoop.main import main

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
    mode : str = None


@app.post("/translate")
async def translate(request_data: TranslationRequest):
    
    try:
        # create temp folder
        temp_folder = tempfile.mkdtemp()
        
        # make subfolders
        inputrml_folder = os.path.join(temp_folder, "inputrml")
        os.makedirs(inputrml_folder)
        rml_file = os.path.join(inputrml_folder, "rml.ttl")

        inputowl_folder = os.path.join(temp_folder, "inputowl")
        os.makedirs(inputowl_folder)
        owl_file = os.path.join(inputowl_folder, "owl.txt")

        inputxsd_folder = os.path.join(temp_folder, "inputxsd") 
        os.makedirs(inputxsd_folder)
        xsd_file = os.path.join(inputxsd_folder, "xsd.xml")

        tempshacl_folder = os.path.join(temp_folder, "tempshacl")
        os.makedirs(tempshacl_folder)

        tempoutput_folder = os.path.join(temp_folder, "output")
        os.makedirs(tempoutput_folder)
        output_file = os.path.join(tempoutput_folder, "output.ttl")

        args = ['-ot', output_file, '--tempshacl_folder', tempshacl_folder, '--mode', request_data.mode]

        # command = f'python scoop/main.py -ot {output_file} --mode{request_data.mode} --tempshacl_folder {tempshacl_folder}'

        priority = ["rmlData", "owlData", "xsdData"]
 
        if request_data.rmlData:
            rdflib.Graph().parse(data=request_data.rmlData, format="turtle").serialize(destination=rml_file, format="turtle")
            # command += f' -m {rml_file} -xr {rml_file}'
            args.extend(['-m', rml_file, '-xr', rml_file])
        elif request_data.owlData:
            open(owl_file, 'w', encoding='utf-8').write(request_data.owlData)
            args.extend(['-o', owl_file])
        elif request_data.xsdData:
            open(xsd_file, 'w').write(request_data.xsdData)
            # command += f' -x {xsd_file}'
            args.extend(['-x', xsd_file])

        # command += f' -ot {output_file}'

        main(args)

        output = rdflib.Graph().parse(output_file, format="turtle")
  
        shutil.rmtree(temp_folder)


        return JSONResponse(content={"shacl_output": output.serialize(format="turtle")})


    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8181)
    # uvicorn.run(app, host="193.190.127.194")
    uvicorn.run(app, host="0.0.0.0")