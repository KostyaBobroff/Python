# -*- encoding: utf-8 -*-
from collections import Counter
import re


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
    logs = list(f)
    f.close()
    # print(len(logs))
    # regexp for URLS
    # <схема>:[//[<логин>:<пароль>@]<хост>[:<порт>]][/]<URL‐путь>[?<параметры>][#<якорь>]
    # ''[a-z]*:[/]{2}[\w]*:?[\w]*@*[\w]*:?[\d]*[^?\s]*'
    urls_counter = Counter()
    for log in logs:
        parser = re.search('[a-z]*:[/]{2}[\w]*:?[\w]*@?[\w]*:?[\d]*[/]?[^?\s]*', log)
        if parser is not None:
            urls_counter[parser.group()] += 1
        # print(parser.group())
    return urls_counter.most_common(5)


#parse()
