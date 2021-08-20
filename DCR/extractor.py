import xml.etree.ElementTree as ET
import  DCR.structure as DCR

#------------------------------------- Extract graph from XML ---------------------------------------#

def graph_from_xml(xml):
    """ Given an DCR Graph in a XML structure, extract a DCR Graph object. """
    graph = DCR.Graph()    
    
    # Extract roles and activities
    for type in ['role', 'activity', 'rule']:
        for highlight in xml.findall(f".//highlights/highlight[@type='{type}']"):
            
            # find element and check it it already exists:
            for item in highlight.findall(".//items/item"):
                ID = item.attrib['id']
            match = False
            for element in graph.get(type):
                if ID == element.ID:
                    match = True
                    case = element
                    break;  
                  
            # If it dosn't exists, create element:
            if match == False:
                if type == 'activity':
                    case = DCR.Activity(ID)
                elif type == 'role':
                    case = DCR.Role(ID)
                elif type == 'rule':
                    case = DCR.Rule(ID)
                # Need more from xml? Add it here    
                
                graph.add(case)

            # Add highlights to element:
            for range in highlight.findall(".//layers/layer/ranges/"):
                h = DCR.Highlight(range.attrib['start'], range.attrib['end'])
                if str(range.text) != "":
                    h.text = range.text
                case.highlights.append(h)
        
    return graph