
# Your access_id and secret_key pair

ID = 'P4c9wtscfsH4rxeT'
KEY = 'i1D0CKk4kVXS0xI1YfN2fJzFVHdW8Y'
assert ID and KEY, 'You must supply your accsess_id and secret key.'
REGION = 'batchcompute.cn-shenzhen.aliyuncs.com'

OSS_HOST = 'oss-cn-shenzhen.aliyuncs.com'
#OSS_HOST='oss-cn-shenzhen-internal.aliyuncs.com'
OSS_BUCKET = 'vp02'
assert OSS_HOST and OSS_BUCKET, 'You also must supply a bucket \
    created with the access_id above.'

IMAGE_ID = 'img-0000000055DBF0650000821C00002121'
assert IMAGE_ID, "You'd better specify a valid image id."

# COUNT_TASK_NUM is the total instance count
TASK_NUM = 1
INSTANCE_NUM = 3
CPU_NUM=16
SYNC=0
M=100

#NFS
LOCK=True
LOCALE='UTF-8'
LOCAL_DATA = '/home/admin/nfs/'


#PATH
PATH_TMPL = 'oss://%s/%s'
REQUEST_NAME='test/data/testString.txt'
RESPONSE_NAME='test/data/testString.txt'
OUTPUTLOG='test/data/testlog%s.txt'
TMPFILE='test/data/tmp.txt'
DATA_PATH = 'test/data/'

PACKAGE_PATH='test/package/udtest.tar.gz'
LOG_PATH=PATH_TMPL%(OSS_BUCKET,'test/logs')
FULL_PACKAGE = PATH_TMPL%(OSS_BUCKET, PACKAGE_PATH)
FULL_DATAPATH=PATH_TMPL%(OSS_BUCKET, DATA_PATH)


