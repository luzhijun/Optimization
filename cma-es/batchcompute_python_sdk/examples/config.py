from batchcompute import CN_SHENZHEN
# Your access_id and secret_key pair
ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'
assert ID and KEY, 'You must supply your accsess_id and secret key.'
REGION = CN_SHENZHEN

OSS_HOST = 'oss-cn-shenzhen.aliyuncs.com'
OSS_BUCKET = 'vp02'
assert OSS_HOST and OSS_BUCKET, 'You also must supply a bucket \
    created with the access_id above.'

IMAGE_ID = 'img-0000000055DBF0650000821C00002121'
assert IMAGE_ID, "You'd better specify a valid image id."

# COUNT_TASK_NUM is the total instance count
COUNT_TASK_NUM = 2
SUM_TASK_NUM = 1

# The start number and end number which
# specify the region you want to find prime
DATA_START = 2
DATA_END = 10000

PATH_TMPL = 'oss://%s/%s'

PACKAGE_PATH = 'batch-python-sdk/package/worker.tar.gz'
# FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)
FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)

DATA_PATH = 'batch-python-sdk/data/'
FULL_DATA = PATH_TMPL%(OSS_BUCKET, DATA_PATH)
LOCAL_DATA = '/Users/trucy/python/batchcompute_python_sdk/examples/'

OUTPUT_PATH = 'batch-python-sdk/output/find_task_result.txt'
COUNT_OUTPUT_PATH = 'batch-python-sdk/output/count_task_result.txt'
FULL_OUTPUT = PATH_TMPL%(OSS_BUCKET, OUTPUT_PATH)

LOG_PATH = 'oss://%s/batch-python-sdk/logs/'%OSS_BUCKET
