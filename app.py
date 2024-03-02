from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import rdflib
import os
import shutil

app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/assets/<path:path>')
# def send_assets(path):
#     return send_from_directory('templates/assets', path)


# @app.route('/examples/<path:path>')
# def send_examples(path):
#     return send_from_directory('templates/examples', path)

# @app.route('/images/<path:path>')
# def send_images(path):
#     return send_from_directory('templates/images', path)

@app.route('/translate', methods=['POST'])
def translate():
    shutil.rmtree('temp_input')
    os.mkdir('temp_input')
    rml_file, owl_file, xsd_file = 'temp_input/rml.ttl', 'temp_input/owl.txt', 'temp_input/xsd.xml'

    shutil.rmtree('temp_output')
    os.mkdir('temp_output')
    output_file = "temp_output/shacl.ttl"

    command = f'python scoop/main.py -ot {output_file}'

    mappings = request.form.get('rmlData')
    if mappings:
        rdflib.Graph().parse(data=mappings, format="turtle").serialize(destination=rml_file, format="turtle")
        command += f' -m {rml_file} -xr {rml_file}'
    
    ontology = request.form.get('owlData')
    if ontology:
        open(owl_file, 'w').write(ontology)
        command += f' -o {owl_file}'

    xsd = request.form.get('xsdData')
    if xsd:
        open(xsd_file, 'w').write(xsd)
        command += f' -x {xsd_file}'

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    output = rdflib.Graph().parse(output_file, format="turtle").serialize(format="turtle")

    if result.returncode == 0:
        shacl_output = result.stdout
        return jsonify({'shacl_output': output})
    else:
        error_message = result.stderr
        return jsonify({'error': error_message}), 500


# if __name__ == '__main__':
#     app.run(debug=True)
#     # app.run(host='0:0:0:0', port=5000, debug=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6942)
