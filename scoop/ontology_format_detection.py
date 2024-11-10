import json

def is_json_ld(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False

def get_ontology_format(data):
    data = "\n".join([line.strip() for line in data.strip().splitlines() if line.strip()])
    
    if is_json_ld(data):
        return 'jsonld'

    elif data.startswith("<?xml") or data.startswith("<rdf:RDF") or data.startswith("<rdf:Description"):
        return 'rdf'

    elif data.startswith("@prefix") or data.startswith("@base"):
        return 'ttl'

    elif all('<' in line and '>' in line and '.' in line and len(line.split()) == 4 for line in data.splitlines()):
        return 'nt'

    elif all('<' in line and '>' in line and '.' in line and len(line.split()) == 5 for line in data.splitlines()):
        return 'nq'

    elif data.count('{') > 0 and data.count('}') > 0:
        return 'trig'

    elif data.startswith("trdf:"):
        return 'trdf'

    elif data.startswith("{") and "rdf:" in data:
        return 'rj'

    elif data.startswith("<rdf:RDF>") and data.count("<rdf:Graph>") > 0:
        return 'trix'

    return 'ttl'

if __name__ == '__main__':

    rdf_strings = [
        '@prefix ex: <http://example.org/> . ex:subject ex:predicate ex:object .',  # Turtle
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">',  # RDF/XML
        '{"@context": {"ex": "http://example.org/"},"@id": "ex:subject", "ex:predicate": "ex:object"}',  # JSON-LD
        '<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> .',  # N-Triples
        '<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> <http://example.org/graph> .',  # N-Quads
        '{<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> .}',  # TriG
        'trdf:{"graph": "ex:graph", "subject": "ex:subject", "predicate": "ex:predicate", "object": "ex:object"}',  # RDF Thrift
        '{"rdf:subject": "ex:subject", "rdf:predicate": "ex:predicate", "rdf:object": "ex:object"}',  # RDF/JSON
        '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Graph><rdf:subject>ex:subject</rdf:subject></rdf:Graph></rdf:RDF>',  # TriX
    ]


    for rdf_string in rdf_strings:
        format_detected = get_ontology_format(rdf_string)
        print(f"Detected RDF format: {format_detected}")
