import pytest
from main import where, aggregate, main
from tabulate import tabulate
import csv
import sys
import pandas as pd


file: list = list(csv.reader(open('products.csv')))
print(tabulate(file[1:], tablefmt="github", headers=file[0]))


def test_where_less():
    result = where(file, "price<300")
    df = pd.read_csv('products.csv')
    df = df[df["price"] < 300].astype(str)
    assert result == [df.columns.tolist()] + df.values.tolist()


def test_where_equal():
    result = where(file, "brand=apple")
    df = pd.read_csv('products.csv')
    df = df[df["brand"] == "apple"].astype(str)
    assert result == [df.columns.tolist()] + df.values.tolist()


def test_where_greater():
    result = where(file, "rating>4.6")
    df = pd.read_csv('products.csv')
    df = df[df["rating"] > 4.6].astype(str)
    assert result == [df.columns.tolist()] + df.values.tolist()


def test_where_wrong_col1(capsys):
    with pytest.raises(SystemExit):
        where(file, "ratin>4.6")
    captured = capsys.readouterr()
    assert "Неверно указано условие фильтрации" in captured.out


def test_where_wrong_col2(capsys):
    with pytest.raises(SystemExit):
        where(file, "ratin=4.6")
    captured = capsys.readouterr()
    assert "Неверно указано условие фильтрации" in captured.out


def test_where_wrong_col3(capsys):
    with pytest.raises(SystemExit):
        where(file, "ratin<4.6")
    captured = capsys.readouterr()
    assert "Неверно указано условие фильтрации" in captured.out


def test_where_wrong_method(capsys):
    with pytest.raises(SystemExit):
        where(file, "rating4.6")
    captured = capsys.readouterr()
    assert "Неверно указано условие фильтрации" in captured.out


def test_aggregate_avg():
    result = aggregate(file, "price=avg")
    df = pd.read_csv('products.csv')
    df = df["price"].mean()
    assert result == [["avg"], [str(df)]]


def test_aggregate_max():
    result = aggregate(file, "rating=max")
    df = pd.read_csv('products.csv')
    df = df["rating"].max()
    assert result == [["max"], [str(df)]]


def test_aggregate_min_price():
    result = aggregate(file, "price=min")
    df = pd.read_csv('products.csv')
    df = df["price"].min()
    assert result == [["min"], [str(float(df))]]


def test_aggregate_wrong_col1(capsys):
    with pytest.raises(SystemExit):
        aggregate(file, "name=avg")
    captured = capsys.readouterr()
    assert "Агрегация данной колонки невозможна" in captured.out


def test_aggregate_wrong_col2(capsys):
    with pytest.raises(SystemExit):
        aggregate(file, "qwer=avg")
    captured = capsys.readouterr()
    assert "Неверно указано условие агрегации" in captured.out


def test_aggregate_wrong_method1(capsys):
    with pytest.raises(SystemExit):
        aggregate(file, "price=avvsad")
    captured = capsys.readouterr()
    assert "Неверно указано условие агрегации" in captured.out


def test_aggregate_wrong_method2(capsys):
    with pytest.raises(SystemExit):
        aggregate(file, "priceavvsad")
    captured = capsys.readouterr()
    assert "Неверно указано условие агрегации" in captured.out


def test_main_no_file(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Пожалуйста введите имя файла" in captured.out


def test_main_wrong_file(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--file", "prdct"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Пожалуйста введите правильное имя файла" in captured.out


def test_main_only_file(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--file", "products.csv"])
    assert tabulate(file[1:], tablefmt="github", headers=file[0])


def test_main(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--file", "products.csv", "--where", "brand=samsung",
                                      "--aggregate", "price=max"])
    main()
    df = pd.read_csv('products.csv')
    df = df[df["brand"] == "samsung"]
    df = df["rating"].max()
    assert tabulate(str(df), tablefmt="github", headers=["max"])
