import json


with open("./output/none_test.json", "r") as f:
    data = json.load(f)
res = []
no_variants = 0
for key in data.keys():
    if data[key]["variants"]:
        # print(key, list(data[key]["variants"].keys()))
        res.append(key)
    else:
        no_variants += 1

print(len(res))
print(no_variants)
print(len(data.keys()))
