import xml.etree.ElementTree as ET

from TCEEC_find_files import find_original_and_c7


def find_root(collection_xml: str):
    tree = ET.parse(collection_xml)
    root = tree.getroot()

    return root


def get_tei_collection_id(root) -> str:
    xml_id = root.attrib["{http://www.w3.org/XML/1998/namespace}id"]

    return xml_id


def find_TEIs_from_root(root):
    tei_list = root.findall("TEI")

    return tei_list


def generate_tei_dict(tei_list):
    tei_dict = {}

    ns = {"letterID": "{http://www.w3.org/XML/1998/namespace}id"}

    for tei in tei_list:
        letterid = tei.get(ns["letterID"])
        # letter_n = int(letterid[-3:])

        tei_dict[letterid] = tei

    return tei_dict


def paragraph_to_text(p_el):
    parts = []

    if p_el.text:
        parts.append(p_el.text)
    for child in p_el:
        parts.append(paragraph_to_text(child))
        if child.tail:
            parts.append(child.tail)

    return "".join(parts)


def get_tei_text(tei):
    textElement = tei.find("text")

    tei_text = ""

    if textElement is not None:
        for paragraph in textElement.findall("p"):
            p_text = paragraph_to_text(paragraph)
            tei_text += p_text + "\n"

    return tei_text


def get_tei_text_by_paragraph(tei):
    textElement = tei.find("text")

    tei_text_by_p = []

    if textElement is not None:
        for paragraph in textElement.findall("p"):
            p_text = paragraph_to_text(paragraph)
            tei_text_by_p.append(p_text)

    return tei_text_by_p


if __name__ == "__main__":

    root = find_root("./data/F2FLEMIN.xml")
    collection_id = get_tei_collection_id(root)
    tei_list = find_TEIs_from_root(root)
    tei_dict = generate_tei_dict(tei_list)
    flemin2_001 = tei_dict["FLEMIN2_001"]

    tei_texts = get_tei_text_by_paragraph(flemin2_001)
    print(tei_texts)
    """
    path = "./data/TCEECE/tceece-collections/"
    res = find_original_and_c7(path)
    print(res)
    print(res["FGIBBON"]["orig"])
    """
