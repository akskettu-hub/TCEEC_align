def get_stats(matched_pairs):
    res = {}

    print(len(matched_pairs))

    for pair in matched_pairs:
        if pair[0] not in res:
            res[pair[0]] = {"total_count": 0, "variants": {}}

        if pair[0] != pair[1]:
            if pair[1] not in res[pair[0]]["variants"]:
                res[pair[0]]["variants"][pair[1]] = {}
                res[pair[0]]["variants"][pair[1]]["count"] = 0

            res[pair[0]]["variants"][pair[1]]["count"] += 1

        res[pair[0]]["total_count"] += 1

    return res


if __name__ == "__main__":
    pass
