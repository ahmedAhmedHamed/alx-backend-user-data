#!/usr/bin/env python3
"""
module to get and obfuscate logs.
"""
from typing import List
import re
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("email", "phone", "ssn", "password", "name")


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
    return re.sub(regexp, r'\1' + redaction + separator, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ custom formatter """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ returns logger for user_data """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ gets db from env credentials """
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    args = {'user': username,
            'host': host,
            'password': password}
    if db_name:
        args['database'] = db_name

    connector = mysql.connector.connect(**args)
    return connector
