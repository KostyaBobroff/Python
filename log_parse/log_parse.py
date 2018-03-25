# -*- encoding: utf-8 -*-
from collections import Counter
import re


def parse_urls(logs, urls_counter):
    for log in logs:
        parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log)
        if parser:
            urls_counter[parser.group()] += 1
    return urls_counter


def parse_urls_without_files(logs, urls_counter):
    for log in logs:
        parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*/', log)
        if parser:
            urls_counter[parser.group()] += 1
    return urls_counter


def parse_urls_without_www(logs, urls_counter):
    for log in logs:
        parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log)

        if parser:
            edit_parser = re.search('(?<=www.)\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*/', parser.group())
            if edit_parser is None:
                edit_parser = parser
            urls_counter[edit_parser.group()] += 1
    return urls_counter


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    f = open("log.log", "r+")
    data = list(f)
    f.close()

    # regexp for URLS
    # <схема>:[//[<логин>:<пароль>@]<хост>[:<порт>]][/]<URL‐путь>[?<параметры>][#<якорь>]
    # [a-z]*:[/]{2}[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*
    # regex для урлов без файлов в листе)
    # (?<=/)[\w]+.[\w]+$
    # regex для урлов когда bool в листе)
    # (?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*/
    urls = Counter()
    urls = parse_urls_without_www(data, urls)

    return urls.most_common(5)

# print(parse())
