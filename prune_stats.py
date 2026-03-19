import json


def open_json():
    with open("./output/none_test.json", "r") as f:
        data = json.load(f)
    return data


def get_variants(data):
    res = {}
    no_variants = 0

    for i in data.keys():
        if data[i]["variants"]:
            res[i] = data[i]

            res[i]["total_variants"] = 0
            for variant in data[i]["variants"].keys():
                res[i]["total_variants"] += data[i]["variants"][variant]["count"]

            res[i]["variants_ratio"] = res[i]["total_variants"] / res[i]["total_count"]

        else:
            no_variants += 1

    # print(len(res.keys()))

    return res


def remove_under_variants_ratio_threshold(data, threshold):
    res = {}
    for key in data.keys():
        if data[key]["variants_ratio"] > threshold:
            res[key] = data[key]

    return res


if __name__ == "__main__":
    data = open_json()
    print(len(data))
    a = get_variants(data)
    # print(a)
    print(len(a.keys()))
    b = remove_under_variants_ratio_threshold(a, 0.75)
    print(len(b.keys()))
    # print(b)
    """
    res_dict_json = json.dumps(b, indent=4, ensure_ascii=False)
    with open("./output/test_prune.json", "w") as f:
        f.write(res_dict_json)
    """
