import re
from datetime import datetime, date, time
from collections import Counter


def parse_urls_without_files(logs):
    # #string = re.sub(r"(?<=./)[-.\w]+[.]\w+(?=[?\s])","",arr[0])
    # for log in logs:
    #     parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log['url'])
    #     if parser and not re.search('\w+\.\w+$',parser.group()):
    for log in logs[:]:
        parser = re.search(r"(?<=./)[-.\w]+[.]\w+(?=[?\s])", log)
        if parser:
            logs.remove(log)
    return logs


def parse_urls(logs, urls_counter):
    for log in logs:
        parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log)
        if parser:
            urls_counter[parser.group()] += 1
    return urls_counter


def parse_ignore_urls(logs, ignore_urls):
    for log in logs[:]:
        parser = re.search('(?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log)
        if parser and parser.group() in ignore_urls:
            logs.remove(log)
    return logs


def parse_urls_without_www(logs):
    return [re.sub(r"(?<=://)www.", "", log) for log in logs]


def start_at_time(logs, start):
    for log in logs[:]:
        parser = re.search("(?<=\[)\d{2}/\w+/\w{4}", log)
        if parser:
            date_from_log = datetime.strptime(parser.group(0), '%d/%b/%Y')
            if start > date_from_log:
                logs.remove(log)
    return logs


def stop_at_time(logs, stop):
    for log in logs[:]:
        parser = re.search("(?<=\[)\d{2}/\w+/\w{4}", log)
        if parser:
            date_from_log = datetime.strptime(parser.group(0), '%d/%b/%Y')
            if stop < date_from_log:
                logs.remove(log)
    return logs


def parse_urls_slow_quire(logs, urls_counter):
    count = Counter()
    for log in logs:
        parser = re.search('(?<=://).*\s([\d]+)(?=\n)', log)
        if parser:
            edit_parser = re.search('^[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', parser.group())
            urls_counter[edit_parser.group()] += int(parser.group(1))
            count[edit_parser.group()] += 1

    for key, elem in urls_counter.items():
        urls_counter[key] = elem // count[key]
    return urls_counter


def parse_by_request_type(logs, request_type):
    for log in logs:
        parser = re.search('(?<=")\w+(?=.*://)', log)
        if parser:
            if request_type != parser.group():
                logs.remove(log)
    return logs


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

    if ignore_files:
        data = parse_urls_without_files(data)
    if ignore_urls:
        data = parse_ignore_urls(data, 'www.sys.mail.ru/calendar/config/254/40263/')
    if ignore_www:
        data = parse_urls_without_www(data)
    if start_at:
        data = start_at_time(data, start_at)
    if stop_at:
        data = stop_at_time(data, stop_at)
    if request_type:
        data = parse_by_request_type(data, request_type)
    urls = Counter()
    if slow_queries:
        urls = parse_urls_slow_quire(data, urls)
    else:
        urls = parse_urls(data, urls)

        # urls = par
    ####datetime.datetime(2005, 7, 14, 0, 0)
    ####d.strftime("%d/%b/%Y")

    # if ignore_files:
    #     log_dict = parse_urls_without_files(data)
    # regexp for URLS
    # <схема>:[//[<логин>:<пароль>@]<хост>[:<порт>]][/]<URL‐путь>[?<параметры>][#<якорь>]
    # [a-z]*:[/]{2}[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*
    # regex для урлов без файлов в листе)
    # (?<=/)[\w]+.[\w]+$
    # regex для урлов когда bool в листе)
    # (?<=//)[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*/
    #  urls = Counter()
    #  urls = parse_urls_without_www(data,urls)

    return urls.most_common(5)

