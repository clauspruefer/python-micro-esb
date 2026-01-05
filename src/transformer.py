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
    """ JSON transfomer class.
    """

    def __init__(self):
        """
        :ivar dict[dict] _json_dict: recursive internal properties processing dict
        """
        self._json_dict = {}

    def json_transform(self):
        """ json_transform() method.

        Recursive generate _json_dict for complete object hierarchy.
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
