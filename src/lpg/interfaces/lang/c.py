"""Project generator for the C language."""


import re

HEADER_FILE_TEMPLATE = "{returnType} {name}({params});"

TEST_FILE_TEMPLATE = """\
#include <stdio.h>

int main() {{
    {param_declarations};
    {returnType} result = {name}({params_call});
    printf("result: %d\\n", result);
    return 0;
}}
"""

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^(?P<returnType>(?:struct )?\w+(?:\[\]|\*)?) (?P<name>\w+)\((?P<params>(?:(?:struct )?\w+(?:\[\]|\*)? \w+(?:, )?)+)\)\s?{$",
    flags=re.MULTILINE,
)


def create_c_project(template: str):
    """Creates the project template for C."""

    match = FUNCTION_SIGNATURE_PATTERN.search(template)
    if match is None:
        raise RuntimeError("Fatal error: project template doesn't match regex.")
    groups = match.groupdict()

    with open("solution.c", "w", encoding="utf-8") as file:
        file.write(template + "\n")

    with open("solution.h", "w", encoding="utf-8") as file:
        file.write(HEADER_FILE_TEMPLATE.format(**groups))

    params = groups["params"].split(", ")
    groups["param_declarations"] = groups["params"].replace(", ", ";\n    ")
    groups["params_call"] = ", ".join(param.split()[-1] for param in params)
    formatted = TEST_FILE_TEMPLATE.format(**groups)

    with open("test.c", "w", encoding="utf-8") as file:
        file.write(formatted)
