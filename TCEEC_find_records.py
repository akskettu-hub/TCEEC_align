import xml.etree.ElementTree as ET
from align_parallel_texts import align_parallel_texts


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


def create_dict(aligned_words):
    res = {}

    for pair in aligned_words:
        if pair[1] not in res:
            res[pair[1]] = 0

        res[pair[1]] += 1

    return res


if __name__ == "__main__":
    root = find_root("./data/F2FLEMIN.xml")
    collection_id = get_tei_collection_id(root)
    tei_list = find_TEIs_from_root(root)
    tei_dict = generate_tei_dict(tei_list)
    flemin2_001 = tei_dict["FLEMIN2_002"]

    tei_texts1 = get_tei_text_by_paragraph(flemin2_001)
    # print(tei_texts1[2])
    # print()

    root = find_root("./data/CEEC-400/CEECE-xml/FFLEMIN2.xml")
    collection_id = get_tei_collection_id(root)
    tei_list = find_TEIs_from_root(root)
    tei_dict = generate_tei_dict(tei_list)
    flemin2_001 = tei_dict["FLEMIN2_002"]

    tei_texts2 = get_tei_text_by_paragraph(flemin2_001)
    # print(tei_texts2[2])
    #

    res = align_parallel_texts(tei_texts1[2], tei_texts2[2])
    for thing in res:
        print(thing)
        print()
    """

    #
    orig = tei_texts2[2]
    norm = tei_texts1[2]

    re_a, re_b = align_parallel_texts(orig, norm)

    print(re_a)
    print(re_b)
    print(len(re_a), len(re_b))
    print(re_a[8], re_b[8])
    print(word_cost(re_a[8], re_b[8]))
    res = align_words(re_a, re_b)

    for item in res:
        if item[0] != item[1]:
            print(item)

    print()
    d = create_dict(res)
    print(json.dumps(d, indent=4))
    """
    """

    a = tokenize_text(orig)
    b = tokenize_text(norm)
    print(len(a), len(b))
    print(a[9], b[9])

    print(word_cost(a[9], b[9]))
    print(res[8])
    print(align_strings(res[8][0], res[8][1]))

    path = "./data/TCEECE/tceece-collections/"
    res = find_original_and_c7(path)
    print(res)
    print(res["FGIBBON"]["orig"])
    """
