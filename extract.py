"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos_collection = []

    try:
        with open(neo_csv_path, 'r') as infile:
            data = list(csv.DictReader(infile))

            neos_collection = [NearEarthObject(designation=data_elem.get('pdes'),
                                               name=data_elem.get('name'),
                                               diameter=data_elem.get(
                                                   'diameter'),
                                               hazardous=data_elem.get('pha'))
                               for data_elem in data]
    except OSError as e:
        print(f"Unable to open {neo_csv_path}:{e}")
    return neos_collection


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    try:
        with open(cad_json_path, 'r') as infile:
            data = json.load(infile)
            data = [dict(zip(data['fields'], data_elem))
                    for data_elem in data['data']]
            approaches = [CloseApproach(designation=data_elem.get('des'),
                                        time=data_elem.get('cd'),
                                        distance=data_elem.get('dist'),
                                        velocity=data_elem.get('v_rel')) for data_elem in data]
    except OSError as e:
        print(f"Unable to open {cad_json_path}:{e}")
    return approaches
