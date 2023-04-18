"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km', 'potentially_hazardous')
    with open(filename, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for close_approach in results:
            info = {**close_approach.serialize(), **
                    close_approach.neo.serialize()}
            info['name'] = info['name'] if info['name'] is not None else ''
            info['diameter_km'] = info['diameter_km'] if (
                info['diameter_km'] != float('nan')) else 'nan'
            writer.writerow(info)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w') as outfile:

        json_data = []
        for close_approach in results:
            info = close_approach.serialize()
            info['neo'] = close_approach.neo.serialize()
            info['neo']['name'] = info['neo']['name'] if info['neo']['name'] is not None else ''
            info['neo']['potentially_hazardous'] = bool(
                1) if info['neo']['potentially_hazardous'] is True else bool(0)
            json_data.append(info)

        json.dump(json_data, outfile, indent=2)
