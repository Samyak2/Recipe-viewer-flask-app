__author__ = 'sheraz/nibesh'

import re

from utils import normalize

MATCHES_RE = re.compile(
    r'^((?:[\d\.,/\s]*)(?:ca\sg|ca|gram|g|mg|kg|ml|cl|liter|dl|l|krm|tsk|msk|port|kruka|krukor)?)?\s*(.+)', re.I)


def parse(st):
    """

    :param st:
    :return:
    """
    st = normalize(st)
    r = MATCHES_RE.match(st)

    res = {
        'measure': str(r.group(1)).strip(),
        'name': r.group(2)
    }
    return res
