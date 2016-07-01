__author__ = 'congrui_li'

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Namespace, RDF
import json
import requests
import multiprocessing
from itertools import chain
import functools
import argparse
from Maybe import *


def load_file(filepath):
    with open(filepath) as _file:
        return _file.read().replace('\n', " ")

AMPO = Namespace("https://tw.rpi.edu/web/project/ampo#")
SIO = Namespace("http://semanticscience.org/ontology/sio.owl#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
PROV = Namespace("http://www.w3.org/ns/prov#")
QUDT = Namespace("http://data.qudt.org/qudt/owl/1.0.0/qudt.owl#")
VITRO = Namespace("http://vitro.mannlib.cornell.edu/ns/vitro/0.7#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
VIVO = Namespace('http://vivoweb.org/ontology/core#')


get_material_query = load_file("queries/listMaterial.rq")
describe_material_query = load_file("queries/describeMaterial.rq")

# standard filters
non_empty_str = lambda s: True if s else False
has_label = lambda o: True if o.label() else False


def get_metadata(id):
    return {"index": {"_index": "ampo", "_type": "material", "_id": id}}


def select(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]


def describe(endpoint, query):
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    try:
        return sparql.query().convert()
    except RuntimeWarning:
        pass


def has_type(resource, type):
    for rtype in resource.objects(RDF.type):
        if str(rtype.identifier) == str(type):
            return True
    return False


def get_material(endpoint):
    r = select(endpoint, get_material_query)
    return [rs["material"]["value"] for rs in r]


def describe_material(endpoint, material):
    q = describe_material_query.replace("?material", "<" + material + ">")
    return describe(endpoint, q)


def get_most_specific_type(material):
    return Maybe.of(material).stream() \
        .flatmap(lambda p: p.objects(VITRO.mostSpecificType)) \
        .map(lambda t: t.label()) \
        .filter(non_empty_str) \
        .one().value


def get_processes(material):
    return Maybe.of(material).stream() \
        .flatmap(lambda p: p.objects(AMPO.isParticipantIn)) \
        .filter(has_label) \
        .map(lambda r: {"uri": str(r.identifier), "name": str(r.label())}).list()


def get_attrs(material):
    return Maybe.of(material).stream() \
        .flatmap(lambda p: p.objects(AMPO.hasAttribute)) \
        .filter(has_label) \
        .map(lambda r: {"uri": str(r.identifier), "name": str(r.label())}).list()


def create_material_doc(material, endpoint):
    graph = describe_material(endpoint=endpoint, material=material)

    mat = graph.resource(material)

    try:
        name = mat.label()
    except AttributeError:
        print("missing name:", material)
        return {}

    doc = {"uri": material, "name": name}

    most_specific_type = get_most_specific_type(mat)
    if most_specific_type:
        doc.update({"mostSpecificType": most_specific_type})

    processes = get_processes(mat)
    if processes:
        doc.update({"process": processes})

    attrs = get_attrs(mat)
    if attrs:
        doc.update({"attr": attrs})

    return doc


def process_material(material, endpoint):
    mat = create_material_doc(material=material, endpoint=endpoint)
    es_id = mat["uri"]
    return [json.dumps(get_metadata(es_id)), json.dumps(mat)]


def publish(bulk, endpoint, rebuild, mapping):
    # if configured to rebuild_index
    # Delete and then re-create to publication index (via PUT request)

    index_url = endpoint + "/ampo"

    if rebuild:
        requests.delete(index_url)
        r = requests.put(index_url)
        if r.status_code != requests.codes.ok:
            print(r.url, r.status_code)
            r.raise_for_status()

    # push current publication document mapping

    mapping_url = endpoint + "/ampo/material/_mapping"
    with open(mapping) as mapping_file:
        r = requests.put(mapping_url, data=mapping_file)
        if r.status_code != requests.codes.ok:

            # new mapping may be incompatible with previous
            # delete current mapping and re-push

            requests.delete(mapping_url)
            r = requests.put(mapping_url, data=mapping_file)
            if r.status_code != requests.codes.ok:
                print(r.url, r.status_code)
                r.raise_for_status()

    # bulk import new publication documents
    bulk_import_url = endpoint + "/_bulk"
    r = requests.post(bulk_import_url, data=bulk)
    if r.status_code != requests.codes.ok:
        print(r.url, r.status_code)
        r.raise_for_status()


def generate(threads, sparql):
    pool = multiprocessing.Pool(threads)
    params = [(material, sparql) for material in get_material(endpoint=sparql)]
    return list(chain.from_iterable(pool.starmap(process_material, params)))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--threads', default=8, help='number of threads to use (default = 8)')
    parser.add_argument('--es', default="http://localhost:9200", help="elasticsearch service URL")
    parser.add_argument('--publish', default=False, action="store_true", help="publish to elasticsearch?")
    parser.add_argument('--rebuild', default=False, action="store_true", help="rebuild elasticsearch index?")
    parser.add_argument('--mapping', default="mappings/material.json", help="publication elasticsearch mapping document")
    parser.add_argument('--sparql', default='https://dofamp.tw.rpi.edu/fuseki/ampo/query', help='sparql endpoint')
    parser.add_argument('out', metavar='OUT', help='elasticsearch bulk ingest file')

    args = parser.parse_args()

    # generate bulk import document for publications
    records = generate(threads=int(args.threads), sparql=args.sparql)

    # save generated bulk import file so it can be backed up or reviewed if there are publish errors
    with open(args.out, "w") as bulk_file:
        bulk_file.write('\n'.join(records)+'\n')

    # publish the results to elasticsearch if "--publish" was specified on the command line
    if args.publish:
        bulk_str = '\n'.join(records)+'\n'
        publish(bulk=bulk_str, endpoint=args.es, rebuild=args.rebuild, mapping=args.mapping)

