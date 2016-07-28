'''Constants used across the BatchCompute SDK package in general.
'''
import sys

# A dictionary to map numeric state to string state.
STATE_MAP = [
    'Init', 'Waiting', 'Running',
    'Finished', 'Failed', 'Stopped'
]

# BatchCompute endpoint information.
ENDPOINT_INFO = {
    'cn-qingdao': 'batchcompute.cn-qingdao.aliyuncs.com',
    'cn-hangzhou': 'batchcompute.aliyuncs.com',
    'cn-shenzhen': 'batchcompute.cn-shenzhen.aliyuncs.com'
}
SERVICE_PORT = 80
CN_QINGDAO = ENDPOINT_INFO['cn-qingdao']
CN_SHENZHEN = ENDPOINT_INFO['cn-shenzhen']

# Api version supported by BatchCompute.
API_VERSION = '2015-06-30'

# Python 2 or Python 3 is in use.
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

# Definition of descriptor types.
if PY2:
    STRING = (str, unicode)
    NUMBER = (int, long)

if PY3:
    STRING = (str, bytes)
    NUMBER = int
TIME = (int, str)
