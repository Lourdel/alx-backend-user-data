#!/usr/bin/env python3
"""Module defines filter_datum function"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Method returns the log message obfuscated"""
    for field in fields:
        pattern = r'{}=(.*?)(?={})'.format(field, separator)
        replacement = '{}={}'.format(field, redaction)
        obfuscated = re.sub(pattern, replacement, message)
    return obfuscated
