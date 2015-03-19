import os
import sys

import eventlet
from oslo.config import cfg

from st2common import log as logging
from st2common.exceptions.sensors import NoSensorsFoundException
from st2common.exceptions.sensors import SensorNotFoundException
from st2common.models.db import db_setup
from st2common.models.db import db_teardown
from st2common.constants.logging import DEFAULT_LOGGING_CONF_PATH
from st2common.transport.utils import register_exchanges
from st2reactor.sensor import config
from st2common.persistence.reactor import SensorType
from st2reactor.container.manager import SensorContainerManager

eventlet.monkey_patch(
    os=True,
    select=True,
    socket=True,
    thread=False if '--use-debugger' in sys.argv else True,
    time=True)


LOG = logging.getLogger('st2reactor.bin.sensors_manager')


def _setup():
    # Set up logger which logs everything which happens during and before config
    # parsing to sys.stdout
    logging.setup(DEFAULT_LOGGING_CONF_PATH)

    # 1. parse config args
    config.parse_args()

    # 2. setup logging.
    logging.setup(cfg.CONF.sensorcontainer.logging)

    # 3. all other setup which requires config to be parsed and logging to
    # be correctly setup.
    username = cfg.CONF.database.username if hasattr(cfg.CONF.database, 'username') else None
    password = cfg.CONF.database.password if hasattr(cfg.CONF.database, 'password') else None
    db_setup(cfg.CONF.database.db_name, cfg.CONF.database.host, cfg.CONF.database.port,
             username=username, password=password)
    register_exchanges()

    # 4. Register internal triggers
    # Note: We need to do import here because of a messed up configuration
    # situation (this module depends on configuration being parsed)
    from st2common.triggers import register_internal_trigger_types
    register_internal_trigger_types()


def _teardown():
    db_teardown()


def _get_all_sensors():
    sensors = SensorType.get_all()
    LOG.info('Found %d sensors.', len(sensors))
    return sensors


def main():
    try:
        _setup()
        container_manager = SensorContainerManager()
        sensors = _get_all_sensors()

        if cfg.CONF.sensor_name:
            # Only run a single sensor
            sensors = [sensor for sensor in sensors if
                       sensor.name == cfg.CONF.sensor_name]
            if not sensors:
                raise SensorNotFoundException('Sensor %s not found in db.' % cfg.CONF.sensor_name)

        if not sensors:
            msg = 'No sensors configured to run. See http://docs.stackstorm.com/sensors.html.'
            raise NoSensorsFoundException(msg)

        return container_manager.run_sensors(sensors=sensors)
    except SystemExit as exit_code:
        return exit_code
    except NoSensorsFoundException as e:
        LOG.exception(e)
        return 0
    except SensorNotFoundException as e:
        LOG.exception(e)
        return 1
    except:
        LOG.exception('(PID:%s) SensorContainer quit due to exception.', os.getpid())
        return 2
    finally:
        _teardown()
