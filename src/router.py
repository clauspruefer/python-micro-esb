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

mod_ref = importlib.import_module('user_routing')


class ServiceRouter():

    def send(self, send_id, metadata):
        logger.info('ServiceRouter send_id:{} metadata:{}'.format(send_id, metadata))
        func_ref = getattr(mod_ref, send_id)
        logger.debug('FuncRef:{}'.format(func_ref))
        return func_ref(metadata)
