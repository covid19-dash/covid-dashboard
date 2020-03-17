import os
import sys

PATTERNS = [
    "/assets",
    "/_dash",
]


def main(argv):
    with open(argv[0], "r") as f:
        content = f.readlines()

    for line_idx in range(len(content)):
        for p in PATTERNS:
            content[line_idx] = content[line_idx].replace(
                p, "/0" + p
            )

    with open(argv[0], "w") as f:
        f.writelines(content)


if __name__ == "__main__":
    main(sys.argv[1:])
