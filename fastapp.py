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
from scoop.SCOOP.shape_integration_priority import ShapeIntegrationPriority
from scoop.SCOOP.shape_integration_priority_r import ShapeIntegrationPriorityR
from scoop.SCOOP.shape_integration_all import ShapeIntegrationAll
from scoop.SCOOP.shape_adjustment_single import ShapeAdjustment

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from scoop.SCOOP.shape_generator.rml2shacl.src.RML import *
from scoop.SCOOP.shape_generator.rml2shacl.src.RMLtoShacl import RMLtoSHACL
from scoop.SCOOP.shape_generator.rml2shacl.src.SHACL import *

from scoop.SCOOP.shape_generator.owl2shacl.src.OWLtoSHACL import translateFromUrl, translateFromFile, translateByJar

from scoop.SCOOP.shape_generator.xsd2shacl.src.XSDtoSHACL import XSDtoSHACL

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
        priority = ["rmlData", "owlData", "xsdData"]

        shapes_graph = []
        for p in priority:
            if p == "rmlData" and request_data.rmlData:
                rmlGraph = rdflib.Graph().parse(data=request_data.rmlData, format="turtle")
                RtoS = RMLtoSHACL()
                rml_shacl_graph = RtoS.evaluate_file(rmlGraph, shacl_path="", write=False)
                shapes_graph.append((rml_shacl_graph,"rml"))

            if p == "owlData" and request_data.owlData:
                owl_shacl_graph = translateFromFile(request_data.owlData)
                shapes_graph.append((owl_shacl_graph,"owl"))

            if p == "xsdData" and request_data.xsdData:
                X2S = XSDtoSHACL()
                xsd_shacl_graph = X2S.evaluate_file(request_data.xsdData)
                if request_data.rmlData:
                    print("Start adjusting shape")
                    sa = ShapeAdjustment("xml")
                    sa.parseRawDataSchemaShape(xsd_shacl_graph)
                    rmlGraph = rdflib.Graph().parse(data=request_data.rmlData, format="turtle")
                    sa.parseRML(rmlGraph)
                    xsd_shacl_graph = sa.adjust(Graph()+xsd_shacl_graph)

                shapes_graph.append((xsd_shacl_graph,"xsd"))
                
        mode = request_data.mode

        if mode == "all":
            shIn = ShapeIntegrationAll(shapes_graph, "")
        elif mode == "priority":
            shIn = ShapeIntegrationPriority(shapes_graph, "")
        elif mode == "priority_r":
            shIn = ShapeIntegrationPriorityR(shapes_graph, "")
        shacl_graph = shIn.integration()
        
        return JSONResponse(content={"shacl_output": shacl_graph.serialize(format="turtle")})

        # if result.returncode == 0:
        #     shacl_output = result.stdout
        #     response = JSONResponse(content={"shacl_output": output})
        #     response.headers["Access-Control-Allow-Origin"] = "*"
        #     response.headers["Access-Control-Allow-Credentials"] = "true"
        #     return response
        # else:
        #     error_message = result.stderr
        #     return JSONResponse(content={"error": error_message}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8181)
    uvicorn.run(app, host="0.0.0.0")