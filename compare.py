import argparse
import ast


def levenshtein_dist(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_dist(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            # j+1 instead of j since
            # previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # then s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def preprocessing_code(code: str) -> str:
    tree = ast.parse(code)
    normalized_code = ast.dump(tree)

    return normalized_code


def compute_plagiarism(s1: str, s2: str) -> float:
    code1 = preprocessing_code(s1)
    code2 = preprocessing_code(s2)
    dist = levenshtein_dist(code1, code2)
    score = 1 - (dist / max(len(code1), len(code2)))

    return score


def parse_input() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('scores', type=str)
    args = parser.parse_args()

    return args.input, args.scores


def read_code(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf8") as f:
        return f.read()


def main() -> None:
    input_file, scores_file = parse_input()

    with open(input_file, 'r', encoding="utf8") as f:
        input_files = list(map(lambda files: files.split(), f.readlines()))

    scores = []
    for file1, file2 in input_files:
        code1 = read_code(file1)
        code2 = read_code(file2)
        score = compute_plagiarism(code1, code2)
        scores.append(str(score))
        print(score)

    with open(scores_file, 'w') as f:
        f.writelines('\n'.join(scores))


if __name__ == '__main__':
    main()

