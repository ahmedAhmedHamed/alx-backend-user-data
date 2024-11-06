#!/usr/bin/env python3
"""
module to get and obfuscate logs.
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    returns the log message obfuscated

    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating
    all fields in the log line (message)

    <FIELD>=<MESSAGE><SEPARATOR>
    we need to capture MESSAGE:
    (field= | field= | field=)("[^<SEPARATOR>]"+)<SEPARATOR>
    replace capture group 2 with xxx
    """
    regexp = '(' + '=|'.join(fields) + '=)' + f'([^{separator}]+)' + separator
    return re.sub(regexp, r'\1xxx' + separator, message)
