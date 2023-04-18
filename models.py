"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """

        def empty_str_check(x): return str(x) if x else None
        def empty_float_check(x): return float(x) if x else float('nan')
        def boolean_check(x): return True if x == 'Y' else False

        self.designation = empty_str_check(info.get('designation'))
        self.name = empty_str_check(info.get('name'))
        self.diameter = empty_float_check(info.get('diameter'))
        self.hazardous = boolean_check(info.get('hazardous'))

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} {self.name}" if self.name else f"{self.designation}"

    def __str__(self):
        """Return `str(self)`. in a human readable format."""
        boolean_txt = 'is' if self.hazardous else 'is not'
        return f"A NearEarthObject {self.fullname} has a diameter of {self.diameter:.3f} km and {boolean_txt} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        """
        Produce a dictionary containing relevant attributes for CSV or JSON serialization.

        Returns: Dict
            A dictionary of serialized information

        """
        serialized_data = {'designation': self.designation, 'name': self.name,
                           'diameter_km': self.diameter, 'potentially_hazardous': self.hazardous}

        return serialized_data


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        def empty_str_check(x): return str(x) if x else None
        def empty_float_check(x): return float(x) if x else 0.0
        def empty_dt_check(x): return cd_to_datetime(x) if x else None

        self._designation = empty_str_check(info.get('designation'))
        self.time = empty_dt_check(info.get('time'))
        self.distance = empty_float_check(info.get('distance'))
        self.velocity = empty_float_check(info.get('velocity'))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return f"{datetime_to_str(self.time)}"

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.neo.fullname}"

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.neo.fullname}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """
        Produce a dictionary containing relevant attributes for CSV or JSON serialization.

        Returns: Dict
            A dictionary of serialized information

        """
        serialized_data = {'datetime_utc': self.time_str,
                           'distance_au': self.distance,
                           'velocity_km_s': self.velocity}

        return serialized_data
