from flask import Blueprint
from psutil import sensors_temperatures, virtual_memory, cpu_percent
from os import getloadavg

bp = Blueprint('api_v1', __name__, url_prefix='/api')

@bp.route('/info', methods = ['GET'])
def system_info():
    return {
        'temp':round(sensors_temperatures()['cpu_thermal'][0].current,2),
        'load':[round(val,2) for val in getloadavg()],
        'cpu':cpu_percent(),
        'ram':virtual_memory().percent,
    }