import os


def find_original_and_c7(path: str):
    file_pairs_d = {}

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        orig_xml = ""
        c7_f_xml = ""

        if os.path.isdir(full_path):
            for file in os.listdir(full_path):
                if file.endswith("c7_formatted.xml"):
                    c7_f_xml = full_path + "/" + file

            for file in os.listdir(full_path + "/orig/"):
                if file.endswith(".xml"):
                    orig_xml = full_path + "/orig/" + file

            file_pairs_d[entry] = {}
            file_pairs_d[entry]["orig"] = orig_xml
            file_pairs_d[entry]["c7"] = c7_f_xml

    return file_pairs_d


def find_original(path: str):
    originals_d = {}

    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)

        orig_xml = ""

        if os.path.isdir(full_path):

            for file in os.listdir(full_path + "/orig/"):
                if file.endswith(".xml"):
                    orig_xml = full_path + "/orig/" + file

            originals_d[entry] = {}
            originals_d[entry]["orig"] = orig_xml

    return originals_d


if __name__ == "__main__":
    res = find_original("./data/TCEECE/tceece-collections/")
    print(res)
    """
    res = find_original_and_c7("./data/TCEECE/tceece-collections/")
    print(res)
    print(res["FGIBBON"]["orig"])
    """
