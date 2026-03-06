import xml.etree.ElementTree as ET

from TCEEC_find_files import find_original_and_c7


def find_root(collection_xml: str):
    tree = ET.parse(collection_xml)
    root = tree.getroot()

    return root


def get_tei_collection_id(collection_xml: str) -> str:
    root = find_root(collection_xml=collection_xml)
    xml_id = root.attrib["{http://www.w3.org/XML/1998/namespace}id"]

    return xml_id


if __name__ == "__main__":
    path = "./data/TCEECE/tceece-collections/"
    res = find_original_and_c7(path)
    print(res)
    print(res["FGIBBON"]["orig"])
