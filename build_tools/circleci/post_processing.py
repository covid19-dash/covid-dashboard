import os
import sys


def inject_index_html(argv):
    with open(argv[0], "r") as f:
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

    with open(argv[0], "w") as f:
        f.writelines(content)


def inject_source_map(argv):
    with open(argv[0], "r") as f:
        content = f.readlines()

    PATTERN = "sourceMappingURL="

    for line_idx in range(len(content)):
        content[line_idx] = content[line_idx].replace(
            PATTERN, PATTERN + "./0/"
        )


if __name__ == "__main__":
    filename = os.path.join(sys.argv[1:], "index.html")
    inject_index_html(filename)
    # TODO: go through each .js and change inject the source map
