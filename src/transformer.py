# ]*[ --------------------------------------------------------------------- ]*[
#  .                  Micro ESB transformer Python Module                    .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer 2016-2026                                       .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import json


class JSONTransformer():
    """ JSON transformer class.

    Provides JSON transformation functionality for class hierarchies.
    """

    def __init__(self):
        """
        :ivar dict _json_dict: recursive internal properties processing dict
        """
        self._json_dict = {}

    def json_transform(self):
        """ json_transform() method.

        Recursively generate _json_dict for complete object hierarchy.

        Iterates through all elements in the hierarchy and calls set_json_dict()
        on each to populate their json_dict representation.
        """

        for element in self.iterate():
            element.set_json_dict()
            self.logger.debug(
                'JSON:{} properties:{}'.format(
                    element.json_dict,
                    element._SYSProperties
                )
            )

    @property
    def json(self):
        """ json() method.

        :return: json.dumps(self._json_dict)
        :rtype: str (json dump)

        Decorated with @property so direct property access possible
        """
        return json.dumps(self._json_dict)

    @property
    def json_dict(self):
        """ json_dict() method.

        :return: self._json_dict
        :rtype: dict

        Decorated with @property so direct property access possible
        """
        return self._json_dict
