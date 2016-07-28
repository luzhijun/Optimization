
# Your access_id and secret_key pair
ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'
assert ID and KEY, 'You must supply your accsess_id and secret key.'
REGION = 'batchcompute.cn-shenzhen.aliyuncs.com'

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

PACKAGE_PATH = 'vpp/package/worker.tar.gz'
# FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)
FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)

DATA_PATH = 'vpp/data/'
FULL_DATA = PATH_TMPL%(OSS_BUCKET, DATA_PATH)
LOCAL_DATA = '/Users/trucy/python/vp/'

FIND_OUTPUT_PATH='vpp/out/find/find_task_result_%s'
OUTPUT_PATH = 'vpp/out/find_task_result.txt'
COUNT_OUTPUT_PATH = 'vpp/out/count_task_result.txt'
FULL_OUTPUT = PATH_TMPL%(OSS_BUCKET, OUTPUT_PATH)

LOG_PATH = 'oss://%s/vpp/logs/'%OSS_BUCKET


