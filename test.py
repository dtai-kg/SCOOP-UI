
import rdflib
import os
import sys
import shutil
from rdflib import Graph
from pyshacl import validate
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

from io import StringIO
import xml.etree.ElementTree as ET


def translate(request_data):
    priority = ["rmlData", "owlData", "xsdData"]
    for p in priority:
        # if p == "rmlData" and request_data:
        #     rmlGraph = rdflib.Graph().parse(data=request_data, format="turtle")
        #     RtoS = RMLtoSHACL()
        #     rml_shacl_graph = RtoS.evaluate_file(rmlGraph, shacl_path="", write=False)
        #     print("OKKKK")
        #     print(rml_shacl_graph.serialize(format="turtle"))
        
        # if p == "owlData" and request_data:
        #     owl_shacl_graph = translateFromFile(request_data)
        #     print("OKKKK")
        #     print(owl_shacl_graph.serialize(format="turtle"))

        if p == "xsdData" and request_data:
            X2S = XSDtoSHACL()
            xsd_shacl_graph = X2S.evaluate_file(request_data)
            print("OKKKK")
            print(xsd_shacl_graph.serialize(format="turtle"))


if __name__ == "__main__":
    
    request_rml = """@prefix rr: <http://www.w3.org/ns/r2rml#>.
    @prefix rml: <http://semweb.mmlab.be/ns/rml#>.
    @prefix ql: <http://semweb.mmlab.be/ns/ql#>.
    @prefix transit: <http://vocab.org/transit/terms/>.
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
    @prefix wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>.
    @base <http://example.com/ns#>.

    <#AirportMapping> a rr:TriplesMap;
    rml:logicalSource [
        rml:source "Airport.csv" ;
        rml:referenceFormulation ql:CSV
    ];
    rr:subjectMap [
        rr:template "http://airport.example.com/{id}";
        rr:class transit:Stop
    ];

    rr:predicateObjectMap [
        rr:predicate transit:route;
        rr:objectMap [
        rml:reference "stop";
        rr:datatype xsd:int
        ]
        ];

    rr:predicateObjectMap [
        rr:predicate wgs84_pos:lat;
        rr:objectMap [
        rml:reference "latitude"
        ]
    ];

    rr:predicateObjectMap [
        rr:predicate wgs84_pos:long;
        rr:objectMap [
        rml:reference "longitude"
        ]
    ].
    """
    request_data = open("test.xml").read()
    translate(request_data)