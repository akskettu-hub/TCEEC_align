import os
import re


def process_HAM(src_HAM_dir_path: str, dest_HAM_dir_path: str) -> None:
    for txt_path in find_HAM(src_HAM_dir_path):
        print(f"processing: {txt_path}...")
        src_HAM = open_file(txt_path)

        # Uncomment line below to remove tags only
        # processed_HAM = remove_tags(src_HAM)

        # Uncomment line below to remove tags and new lines
        # processed_HAM = remove_tags(remove_newline(src_HAM))

        # Uncomment line below to remove tags, new lines, and double spaces.
        processed_HAM = remove_double_space(remove_tags(remove_newline(src_HAM)))

        # Uncomment line below to remove tags, new lines, double spaces, and hyphen remnants.
        processed_HAM = remove_hyphenated(
            remove_double_space(remove_tags(remove_newline(src_HAM)))
        )

        dest = dest_HAM_dir_path + os.path.basename(txt_path)

        save_file(dest_path=dest, txt=processed_HAM)


def find_HAM(HAM_dir_path: str) -> list[str]:
    res = []
    for path in os.listdir(HAM_dir_path):
        if path.endswith(".txt"):
            full_path = os.path.join(HAM_dir_path, path)
            res.append(full_path)

    return res


def open_file(path: str) -> str:
    with open(path, "r") as f:
        txt = f.read()

    return txt


def remove_newline(text: str) -> str:
    return text.replace("\n", " ")


def remove_double_space(text: str) -> str:
    return text.replace("  ", " ")


def remove_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def remove_hyphenated(text: str) -> str:
    return text.replace("= =", "")


def save_file(dest_path: str, txt: str) -> None:
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    process_HAM(
        "./data/HAM_TXT_files_(normalised)_20260213/",
        "./output/HAM_TXT_files_(normalised)_20260213_(tags_and_newline_removed)/",
    )
    process_HAM(
        "./data/HAM_TXT_files_(diplomatic)_20260213/",
        "./output/HAM_TXT_files_(diplomatic)_20260213_(tags_and_newline_removed)/",
    )
