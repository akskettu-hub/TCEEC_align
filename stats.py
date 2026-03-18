def get_stats(matched_pairs, stats_dict={}, to_lower=False):
    for pair in matched_pairs:
        a = pair[0]
        b = pair[1]
        if to_lower:
            if a:
                a = a.lower()
            if b:
                b = b.lower()
        if a not in stats_dict:
            stats_dict[a] = {"total_count": 0, "variants": {}}

        if a != b:
            if b not in stats_dict[a]["variants"]:
                stats_dict[a]["variants"][b] = {}
                stats_dict[a]["variants"][b]["count"] = 0

            stats_dict[a]["variants"][b]["count"] += 1

        stats_dict[a]["total_count"] += 1

    return stats_dict


if __name__ == "__main__":
    pass
