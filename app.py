from flask import Flask, request
import xml.etree.ElementTree as ET
from DCR.compare import Compare, Evaluator
import DCR.extractor as extract

app = Flask(__name__)

#   COMPARE HIGHLIGHTS ALGORITHM
#   Given two graphs, compare them by identifying highlight matches.
#   Created 29.07.21, Rasmus Iven Strømsted, DCR Solutions

@app.route('/', methods=['POST'])
def home():
    """ Main function handling user request through REST. Expects a XML format, providing a list of compare types('ACTIVITY', 'ROLE', and 'RULE'), 
    a list of comparison methods('spans', 'labels', and 'compositions'), an evaluation method('source_intersection' or 'union') and two DCR Graphs.
    The function will return a similarity score and a list of the matching graph components."""
    
    # XML request:
    data = request.data
    xml = ET.fromstring(data)
    
    # Extract the DCR component types, the user wants to compare:
    user_types = []
    for compare_type in xml.findall(".//compare_types/type"):
        user_types.append(compare_type.text)
    print("compare_types: ", user_types)
    # Extract the methods the user wants to use for comparison:
    user_compare_methods = []
    for compare_method in xml.findall(".//compare_methods/compare_method"):
        user_compare_methods.append(compare_method.text)
    print("compare_methods: ", user_compare_methods)
     # Extract the evaluation method the user wants to use for comparison:
    user_input_evaluation = []
    for evaluation_method in xml.findall(".//evaluation_methods/evaluation_method"):
        user_input_evaluation.append(evaluation_method.text)  
    print("user_input_evaluation: ", user_input_evaluation)    
    # Extract Source graph: 
    for xml_graph in xml.findall('.//source_graph/*'):
        source = extract.graph_from_xml(xml_graph)
        
    # Extract Target graph:
    for xml_graph in xml.findall('.//target_graph/*'):
        target = extract.graph_from_xml(xml_graph)
    
    # Compare source and target graphs, and get a simularity score:
    comparison = Compare(source, target, user_types, user_compare_methods)
    score = Evaluator(comparison, user_input_evaluation[0]).simularity

    return {"score": score, "intersection": comparison.intersection.__dict__}

if __name__ == '__name__':
    app.run()   

app.run(port=5000)