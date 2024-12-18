# ]*[ --------------------------------------------------------------------- ]*[
#  .                  Micro ESB transformer Python Module                    .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer 2016-2024                                       .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import json
import copy


class JSONTransformer(object):
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

        root_instance = copy.copy(self)

        for element in root_instance.iterate():
            element.set_json_dict()
            self.logger.debug('JSON:{} properties:{}'.format(
                    element.json_dict,
                    element._SYSProperties
                )
            )

        while root_instance.class_count > 0:
            for element in root_instance.iterate():
                if element.class_count == 0 and element._SYSType != 'multiclass_instance':
                    cname = element.class_name
                    parent_element = element.parent_object
                    parent_element._json_dict[cname] = element.json_dict[cname]
                    class_names_list = parent_element._SYSClassNames
                    del class_names_list[class_names_list.index(cname)]

        self._json_dict = root_instance.json_dict
        del root_instance

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
