import os
import xml.etree.ElementTree as ET
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef

def convert_full_tei_to_turtle():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    xml_path = os.path.join(project_root, "theCountOfMonteCristo.xml")
    output_ttl_path = os.path.join(project_root, "output_rdf.ttl")
    
    print(f"Full reading and parsing of the XML file from: {xml_path}")

    g = Graph()

    TEI_NS = {'tei': 'http://www.tei-c.org/ns/1.0'}
    
    # Initializing the main Namespaces (I chose to declare the others only when needed, a personal preference).
    EX = Namespace("http://example.org/monte-cristo/")
    SCHEMA = Namespace("http://schema.org/")
    FOAF = Namespace("http://xmlns.com/foaf/0.1/")
    DCTERMS = Namespace("http://purl.org/dc/terms/")
    CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")

    g.bind("ex", EX)
    g.bind("schema", SCHEMA)
    g.bind("foaf", FOAF)
    g.bind("dcterms", DCTERMS)
    g.bind("crm", CRM)

    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Retrieve all the information from <listPerson>
    for person in root.findall('.//tei:person', TEI_NS):
        p_id = person.get('{http://www.w3.org/XML/1998/namespace}id') or person.get('xml:id')
        if not p_id:
            continue
        
        subject = EX[p_id]
        g.add((subject, RDF.type, FOAF.Person))
        
        same_as = person.get('sameAs')
        if same_as:
            g.add((subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(same_as)))
            
        role = person.get('role')
        if role:
            g.add((subject, EX['role'], Literal(role)))
            
        pers_name = person.find('tei:persName', TEI_NS)
        if pers_name is not None and pers_name.text:
            g.add((subject, FOAF.name, Literal(pers_name.text.strip())))
            
        birth = person.find('tei:birth', TEI_NS)
        if birth is not None and birth.text:
            g.add((subject, SCHEMA.birthDate, Literal(birth.text.strip())))
            
        death = person.find('tei:death', TEI_NS)
        if death is not None and death.text:
            g.add((subject, SCHEMA.deathDate, Literal(death.text.strip())))

    # Retrieve all the information from <listObject>
    for obj in root.findall('.//tei:object', TEI_NS):
        o_id = obj.get('{http://www.w3.org/XML/1998/namespace}id') or obj.get('xml:id')
        if not o_id:
            continue
            
        subject = EX[o_id]
        obj_type = obj.get('type')
        if obj_type:
            g.add((subject, EX['objectType'], Literal(obj_type)))
            
        obj_name = obj.find('.//tei:objectName', TEI_NS)
        if obj_name is not None and obj_name.text:
            g.add((subject, SCHEMA.name, Literal(obj_name.text.strip())))

    # Retrieve all the information from <listPlace>
    for place in root.findall('.//tei:place', TEI_NS):
        pl_id = place.get('{http://www.w3.org/XML/1998/namespace}id') or place.get('xml:id')
        if not pl_id:
            continue
            
        subject = EX[pl_id]
        g.add((subject, RDF.type, CRM.E53_Place))
        
        same_as = place.get('sameAs')
        if same_as:
            g.add((subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(same_as)))
            
        place_name = place.find('tei:placeName', TEI_NS)
        if place_name is not None and place_name.text:
            g.add((subject, SCHEMA.name, Literal(place_name.text.strip())))

    # Retrieve all the information from <listBibl>
    for bibl in root.findall('.//tei:bibl', TEI_NS):
        b_id = bibl.get('{http://www.w3.org/XML/1998/namespace}id') or bibl.get('xml:id')
        if not b_id:
            continue
            
        subject = EX[b_id]
        g.add((subject, RDF.type, DCTERMS.BibliographicResource))
        
        same_as = bibl.get('sameAs')
        if same_as:
            g.add((subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(same_as)))
            
        title = bibl.find('tei:title', TEI_NS)
        if title is not None and title.text:
            g.add((subject, DCTERMS.title, Literal(title.text.strip())))
            
        date = bibl.find('tei:date', TEI_NS)
        if date is not None and date.text:
            g.add((subject, DCTERMS.date, Literal(date.text.strip())))

    # Retrieve all the information from <listRelation>
    list_relation = root.find('.//tei:listRelation', TEI_NS)
    if list_relation is not None:
        for relation in list_relation.findall('tei:relation', TEI_NS):
            rel_name = relation.get('name')
            active = relation.get('active')
            passive = relation.get('passive')
            
            if rel_name and active and passive:
                subj_id = active.lstrip('#')
                subject = EX[subj_id]
                
                if rel_name == "rdf:type":
                    predicate = RDF.type
                elif ":" in rel_name:
                    prefix, local_name = rel_name.split(":", 1)
                    ns_map = {
                        "dcterms": DCTERMS,
                        "prov": Namespace("http://www.w3.org/ns/prov#"),
                        "frbroo": Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/"),
                        "bf": Namespace("http://id.loc.gov/ontologies/bibframe/"),
                        "schema": SCHEMA,
                        "sl": Namespace("http://www.sealitproject.eu/ontology/"),
                        "crm": CRM,
                        "foaf": FOAF,
                        "wdt": Namespace("http://wikidata.org/prop/direct/")
                    }
                    predicate = ns_map.get(prefix, EX)[local_name]
                else:
                    predicate = EX[rel_name]
                
                if passive.startswith("http://") or passive.startswith("https://"):
                    obj = URIRef(passive)
                elif ":" in passive and not passive.startswith("#"):
                    p_prefix, p_local = passive.split(":", 1)
                    p_ns_map = {
                        "foaf": FOAF,
                        "frbroo": Namespace("http://iflastandards.info/ns/fr/frbr/frbroo/"),
                        "sl": Namespace("http://www.sealitproject.eu/ontology/"),
                        "wdt": Namespace("http://wikidata.org/prop/direct/"),
                        "crm": CRM,
                        "dcterms": DCTERMS
                    }
                    obj = p_ns_map.get(p_prefix, EX)[p_local]
                else:
                    obj_id = passive.lstrip('#')
                    obj = EX[obj_id]
                
                g.add((subject, predicate, obj))

    # Serialize the graph and store the RDF data created on a dedicated Turtle file
    g.serialize(destination=output_ttl_path, format="turtle")
    print(f"Conversion complete! Turtle file successfully generated in: {output_ttl_path}")

if __name__ == "__main__":
    convert_full_tei_to_turtle()