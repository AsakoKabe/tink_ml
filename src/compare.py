import argparse

from levenshtein import levenshtein_dist
from preprocessing import normalizing_code


def compute_plagiarism(s1: str, s2: str) -> float:
    code1 = normalizing_code(s1)
    code2 = normalizing_code(s2)
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

    with open(scores_file, 'w') as f:
        f.writelines('\n'.join(scores))


if __name__ == '__main__':
    main()
