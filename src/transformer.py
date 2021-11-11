# ]*[ --------------------------------------------------------------------- ]*[
#  .                     Micro ESB handler Python Module                     .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer 2016-2018                                       .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

# -*- coding:utf-8 -*-

import json
import copy


class JSONTransformer(object):
    """ JSON transfomer class.
    """

    def __init__(self):
        self._json_dict = {}

    def json_transform(self):

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
        return json.dumps(self._json_dict)

    @property
    def json_dict(self):
        return self._json_dict
