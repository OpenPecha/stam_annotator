from typing import List


def add_newlines_around_hashes(input_string):
    lines = input_string.split("\n")

    processed_lines: List[str] = []

    for i, line in enumerate(lines):
        if line.startswith("#"):
            # Add a newline before the '#' line if the previous line is not already a newline
            # and it's not the first line of the text
            if i > 0 and processed_lines[-1] != "":
                processed_lines.append("")
            processed_lines.append(line)
            # Add a newline after the '#' line if it's not the last line and the next line is not already a newline
            if i < len(lines) - 1 and lines[i + 1] != "":
                processed_lines.append("")
        else:
            processed_lines.append(line)

    # Join the processed lines back into a single string
    output_string = "\n".join(processed_lines)
    return output_string
