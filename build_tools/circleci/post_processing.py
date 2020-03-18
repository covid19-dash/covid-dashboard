import os
import sys


def inject_index_html(filename):
    with open(filename, "r") as f:
        content = f.readlines()

    PATTERNS = [
        "/assets",
        "/_dash",
    ]

    for line_idx in range(len(content)):
        for p in PATTERNS:
            content[line_idx] = content[line_idx].replace(
                p, "/0" + p
            )

    with open(filename, "w") as f:
        f.writelines(content)


def inject_source_map(filename):
    try:
        with open(filename, "r") as f:
            content = f.readlines()
    except:
        return

    PATTERN = "sourceMappingURL="

    for line_idx in range(len(content)):
        content[line_idx] = content[line_idx].replace(
            PATTERN, PATTERN + "./0/"
        )

    with open(filename, "w") as f:
        f.writelines(content)


if __name__ == "__main__":
    filename = os.path.join(sys.argv[1], "index.html")
    inject_index_html(filename)
    for root, dirs, files in os.walk(sys.argv[1]):
        for f in files:
            inject_source_map(os.path.join(root, f))
