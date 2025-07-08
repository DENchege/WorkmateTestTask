import csv
import argparse
from tabulate import tabulate


def where(file: list, cond: str) -> list:
    ret: list = list()
    if '<' in cond:
        name, value = cond.split('<')
        try:
            col: int = file[0].index(name)
        except ValueError:
            print("Неверно указано условие фильтрации")
            exit()
        for row in file[1:]:
            if float(row[col]) < float(value):
                ret.append(row)
    elif '=' in cond:
        name, value = cond.split('=')
        try:
            col: int = file[0].index(name)
        except ValueError:
            print("Неверно указано условие фильтрации")
            exit()
        for row in file[1:]:
            if row[col] == value:
                ret.append(row)
    elif '>' in cond:
        name, value = cond.split('>')
        try:
            col: int = file[0].index(name)
        except ValueError:
            print("Неверно указано условие фильтрации")
            exit()
        for row in file[1:]:
            if float(row[col]) > float(value):
                ret.append(row)
    else:
        print("Неверно указано условие фильтрации")
        exit()
    return [file[0]] + ret


def aggregate(file: list, cond: str) -> list:
    ret: list = list()
    if "=" not in cond:
        print("Неверно указано условие агрегации")
        exit()
    name, method = cond.split('=')
    try:
        col: int = file[0].index(name)
    except ValueError:
        print("Неверно указано условие агрегации")
        exit()
    try:
        float(file[1][col])
    except ValueError:
        print("Агрегация данной колонки невозможна")
        exit()
    if method == 'avg':
        choice: list = list()
        for row in file[1:]:
            choice.append(float(row[col]))
        ret = [['avg'], [str(sum(choice) / len(choice))]]
    elif method == 'max':
        choice: list = list()
        for row in file[1:]:
            choice.append(float(row[col]))
        ret = [['max'], [str(max(choice))]]
    elif method == 'min':
        choice: list = list()
        for row in file[1:]:
            choice.append(float(row[col]))
        ret = [["min"], [str(min(choice))]]
    else:
        print("Неверно указано условие агрегации")
        exit()
    return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--where')
    parser.add_argument('--aggregate')
    args = parser.parse_args()

    try:
        file: list = list(csv.reader(open(args.file)))
    except FileNotFoundError:
        print("Пожалуйста введите правильное имя файла")
        raise SystemExit()
    except TypeError:
        print("Пожалуйста введите имя файла")
        raise SystemExit()

    out: list = list()
    if args.where:
        out = where(file, args.where)
    else:
        out = file
    if args.aggregate:
        out = aggregate(out, args.aggregate)

    print(tabulate(out[1:], tablefmt="github", headers=out[0]))


if __name__ == "__main__":
    main()
