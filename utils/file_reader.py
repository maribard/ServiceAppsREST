import json
from pathlib import Path

BASE_PATH = Path.cwd().joinpath('data')


def read_file(file_name):
    """
    Open the file, read it
    :param file_name: File name
    :return: Deserialized JSON doc to Python object
    """
    path = get_file_with_json_extension(file_name)

    with path.open(mode='r') as f:
        return json.load(f)


def write_file(file_name, dumpdate):
    """
    Open the file, write data
    :param file_name: File name
    :param dumpdate: Data to write
    :return: Serialized object as a JSON
    """
    path = get_file_with_json_extension(file_name)

    with path.open(mode='w') as f:
        return json.dump(dumpdate, f)


def get_file_with_json_extension(file_name):
    if '.json' in file_name:
        path = BASE_PATH.joinpath(file_name)
    else:
        path = BASE_PATH.joinpath(f'{file_name}.json')
    return path