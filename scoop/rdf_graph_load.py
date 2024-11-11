import rdflib
import logging

logging.basicConfig(level=logging.ERROR)

def load_rdf_graph(data):
    formats = ['turtle', 'nt', 'xml', 'json-ld', 'n3', 'trig', 'trix', 'nquads']
    for fmt in formats:
        graph = rdflib.Graph()
        try:
            graph.parse(data=data, format=fmt)
            return graph, fmt
        except:
            continue

    return None, None

if __name__ == '__main__':
    rdf_strings = [
        '@prefix ex: <http://example.org/> . ex:subject ex:predicate ex:object .',  # Turtle
        '{"@context": {"ex": "http://example.org/"},"@id": "ex:subject", "ex:predicate": "ex:object"}',  # JSON-LD
        '<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> .',  # N-Triples
        '<http://example.org/subject> <http://example.org/predicate> <http://example.org/object> <http://example.org/graph> .',  # N-Quads
    ]

    for rdf_string in rdf_strings:
        graph, rdf_format = get_rdf_format(rdf_string)
        print(f"Detected RDF format: {rdf_format}, Graph: {graph}")
