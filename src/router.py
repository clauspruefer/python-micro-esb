# ]*[ --------------------------------------------------------------------- ]*[
#  .                     Micro ESB Router Python Module                      .
# ]*[ --------------------------------------------------------------------- ]*[
#  .                                                                         .
#  .  Copyright Claus Prüfer 2016-2026                                       .
#  .                                                                         .
#  .                                                                         .
# ]*[ --------------------------------------------------------------------- ]*[

import logging
import importlib

logger = logging.getLogger(__name__)

try:
    mod_ref = importlib.import_module('user_routing')
except ImportError as e:
    pass


class ServiceRouter():
    """ ServiceRouter class.

    Provides routing functionality to user-defined service methods in user_routing module.
    """

    def send(self, send_id, metadata):
        """ send() method.

        Execute method with given id in `send_id` from imported user_routing.py module
        and return result dict or None.

        :param str send_id: service method id (function name in user_routing module)
        :param dynamic metadata: first argument passed to service method function
        :return: result from user routing function
        :rtype: dict | None
        """
        logger.debug('ServiceRouter send_id:{} metadata:{}'.format(send_id, metadata))
        func_ref = getattr(mod_ref, send_id)
        logger.debug('FuncRef:{}'.format(func_ref))
        return func_ref(metadata)
