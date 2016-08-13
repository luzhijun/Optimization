
# v20150630 相关说明


## 1、 安装

* 通过setuptools安装，下载安装包并解压为batchcompute_python_sdk；

```bash
$ cd batchcompute_python_sdk
$ sudo python setup.py install
```

* 通过pip安装，python2.5以上版本可以直接通过pip安装；

```bash
$ sudo pip install -U setuptools
$ sudo pip install batchcompute
```

* 验证安装，执行以下命令，如果不报错代表安装成功；

```bash
$ python
>>> import batchcompute
>>> batchcompute.__version__
```

## 2、 SDK 的使用

> 您必须替换代码中的`endpoint`，`access_key_id`，`access_key_secret`等用户信息以及worker路径和其他oss相关的路径。

```python
import time

from batchcompute import JobDescription, Client, CN_QINGDAO

endpoint = CN_QINGDAO 
access_key_id = ... # your_access_key_id
access_key_secret = ... # your_access_key_secret

client = Client(endpoint, access_key_id, access_key_secret, human_readable=True)

job_json = '''{
    "JobName": "find-prime",
    "JobTag": "Batchcompute",
    "TaskDag": {
        "TaskDescMap": {
            "Find": {
                "PackageUri": "oss://your-bucket/batch_python_sdk/worker.tar.gz",
                "ProgramName": "find_prime_worker.py",
                "ProgramType": "python",
                "InstanceCount": 1,
                "ResourceDescription": {
                    "Cpu": 800,
                    "Memory": 2000
                },
                "EnvironmentVariables": {},
                "ImageId": "img-xxxx",
                "StdoutRedirectPath": "oss://your-bucket/batch_python_sdk/logs/",
                "StderrRedirectPath": "oss://your-bucket/batch_python_sdk/logs/"
            }
        },
        "Dependencies": {}
    }
}'''

job_desc = JobDescription(job_json)

# Create jobs.
job = client.create_job(job_desc)

while(True):
    # Get job status.
    job_status = client.get_job(job)
    if job_status.State in ['Waiting', 'Running']:
        print('Job %s is %s now.' % (job, job_status.State))
        time.sleep(3)
        continue
    else:
        # 'Failed', 'Stopped', 'Finished'.
        print('Job %s is %s now.' % (job, job_status.State))
        break

```

## 3、 类和常量

| 序号 | 名称 | 可序列化 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1.  | __Client__ | No | 与BatchCompute服务交互的客户端类型 |
| 2.  | __JobDescription__ | Yes | 描述用户作业的类 |
| 3.  | __TaskDag__ | Yes |描述作业任务以及任务间互相之间依赖关系的类 |
| 4.  | __TaskDescription__ | Yes | 描述任务的类 |
| 5.  | __ResourceDescription__ | Yes | 描述任务对CPU, Memory资源需求的类 |
| 6.  | __Job__ | Yes | 描述给定作业当前状态信息的类 |
| 7.  | __Task__ | Yes | 描述给定的作业任务的当前状态信息的类 |
| 8.  | __Instance__ | Yes | 描述给定的任务实例当前状态信息的类 |
| 9.  | __Image__ | Yes |描述给定镜像的信息的类 |
| 10. | __CreateResponse__ | No | 创建新作业时Client返回的响应类 |
| 11. | __GetResponse__ | No | 获取作业状态及作业描述时，Client返回的响应类 |
| 12. | __ActionResponse__ | No | 对作业尽行开始、停止或者删除等操作时由Client返回的响应类
| 13. | __ListResponse__ | No | 列举所有作业和镜像时，由Client返回的响应类 |
| 14. | __CN_QINGDAO__ | No | 常量，BatchCompute的青岛endpoint |


### 关于类属性  
> 除了Client类型，SDK中的大部分类型均具有各种属性。属性均可以通过其名称直接读取，例如，你可以通过如下代码获取作业ID:  
> 另外属性名与Python规范[PEP8][pep8]中类的命名方式保持一致(区别于类方法的命名规则)，遵循[CamelCase][wiki camel case]的拼写规则.  

[wiki camel case]: https://en.wikipedia.org/wiki/CamelCase
[pep8]: https://www.python.org/dev/peps/pep-0008/

```python
# job is a Job object.
job = ...

job_id = job.JobId
print(job_id)

```

* 另外，可以通过字典取值的方式获取属性，例如：

```python
# job is a Job object.
job = ...

job_id = job['JobId']
print(job_id)

```

* 对于类 `JobDescription`, `TaskDag`, `Task`, `ResourceDescription`, 可以通过赋值的方式更改某个属性的值,例如:

```python
from batchcompute import JobDescription

job_desc = JobDescription()
job_desc.JobName = 'find-prime'

```

* 对于类 `JobDescription`, `TaskDag`, `TaskDescription`, `ResourceDescription`, 可以通过字典的方式对类的属性进行赋值, 例如:

```python
from batchcompute import JobDescription

job_desc = JobDescription()
job_desc['JobId'] = 'find-prime'

```

### 关于可序列化
> SDK中所有可序列化的类均从内部类型 `Jsonizable` 继承而来，以下是关于 `Jsonizable` 类型及其子类的描述；

**参数说明：**
> `Jsonizable` 及其子类对象均可通过字典，`Jsonizable` 对象或者描述字典的JSON串初始化。
> 注意，在初始化 `Jsonizable` 对象及其子类时，会丢弃字典或者json串中所有不合法的属性描述信息。

| 参数 | 类型 | 描述 |
| :-----: | :----: | ---- |
| __properties__ | dict, str, Jsonizable object| 属性描述信息 |

* 通过字典初始化 `Jsonizable` 类:

e.g.
```python
from batchcompute import JobDescription

# A dict object.
properties = {
    "JobName": "find-prime",
    "JobTag": "Batchcompute"
}

jsonizable = JobDescription(properties)
print(jsonizable.JobName)
print(jsonizable.JobTag)

```

* 通过JSON字符串初始化 `Jsonizable` 类

e.g.
```python
from batchcompute import JobDescription

# A string jsonized from a dict object.
properties = '''{
    "JobName": "find-prime",
    "JobTag": "Batchcompute"
}'''

jsonizable = JobDescription(properties)
print(jsonizable.JobName)
print(jsonizable.JobTag)

```

* 通过相同类的对象初始化 `Jsonizable` 类。

e.g.
```python
form batchcompute import JobDescription

# A JobDescription object.
jsonizable1 = JobDescription()
jsonizable1.JobName = 'find-prime'
jsonizable1.JobTag = 'Batchcompute'

jsonizable2 = JobDescription(jsonizable1)
print(jsonizable2.JobName)
print(jsonizable2.JobTag)

```

**方法说明：**

| 序号 | 方法名 | 描述 |
| :-----: | :----: | ---- |
| 1. | __update__ | 接受一个字典对象，更新类的部分属性，不合法的属性将被丢弃 |
| 2. | __detail__ | 返回一个包含类属性的字典，如果属性为空将不被包含 |
| 3. | __load__ | 接受一个字符串，该字符串是一个json化的字典，类的属性均被更新，不合法的属性会被丢弃 |
| 4. | __dump__ | 返回一个字符串，内容json化的字典，包含所有类属性信息，如果属性为空将不被包含 |
| 5. | __\_\_str____ | 被print调用的内置函数，其内部调用了dump函数 |


### 关于响应类
> 所有的返回类 (`CreateResponse`, `GetResponse`, `ActionRespnse`, `ListResponse`)均继承内部类型`RawResponse`.
> 以下描述适用于所有的`RawResponse`的子类。

**属性说明：**

| 属性 | 类型 | 描述 |
| :-----: | :----: | ---- |
| __RequestId__ | str | Client的所有请求的识别码 |
| __StatusCode__ | int | Client的所有请求的状态码 |

e.g.
```python

...

response = client.create_job(job_desc)

print response.RequestId
print response.StatusCode

```

## 4. Client 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __endpoint__ | str | 可用的BatchCompute域名或region |
| __access_key_id__ | str | 用户的Aliyun access key id |
| __access_key_secret__ | str | 用户的Aliyun access key secret |
| __human_readable__ | bool | 是否格式化输出时间戳信息 |

e.g.
```python
from batchcompute import Client, CN_QINGDAO

endpoint = CN_QINGDAO 
access_key_id = ... # your_access_key_id
access_key_secret = ... # your_access_key_secret

client = Client(endpoint, access_key_id, access_key_secret, human_readabel=True)

# You can enjoy Batchcompute through this `client` now!
...
```

### 4.1 create_job

**参数说明：**
> 所有类型的参数将被转换为包含属性信息的字典对象。

| 参数 | 类型 | 描述 |
|:------:|:------:|--------|
| __job_desc__ | JobDescription object, str, dict | Job的简单描述和Job对象中有各个任务的描述信息，以及各个任务之间的DAG依赖 |

**返回值说明：**
> create_job 方法将返回一个`CreateResponse`对象, 以下是 `CreateResponse` 对象的属性, 可以通过 `response.JobId` 的方式获取新任务的ID。

| 属性 | 类型 | 描述 |
|:------:|:------:|--------|
| __JobId__ | str | 新任务的任务ID |

e.g.
```python
try:
    # Init a Client object.
    client = ...

    # Refer to JobDescription class to have a look at how to create a new job description.
    job_desc = JobDescription(...)

    job = client.create_job(job_desc)
    # Print out the job id.
    print(job.JobId)
except ClientError, e:
    print(e)
```

#### （1）JobDescription 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, JobDescription object | 包含作业描述信息的对象 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1. | __JobName__ | str | 作业名称 |
| 2. | __Priority__ | int | 优先级用一个[0,1000]范围内的整数指定。数值越高表示作业调度时的优先级越高 |
| 3. | __Description__ | str | 作业的简短描述信息 |
| 4. | __TaskDag__ | TaskDag object | Job对象中有各个任务的描述信息，以及各个任务之间的DAG依赖 |

e.g.

* 可以通过赋值一一设置作业的描述信息。

```python
from batchcompute import JobDescription, TaskDag, ResourceDescription

# Refer to TaskDag class to have a look at how to create a TaskDag.
task_dag = ... # A TaskDag object.

job_desc = JobDescription()
job_desc.JobName = 'find-prime'
job_desc.JobTag = 'Batchcompute'
job_desc.TaskDag = task_dag
job_desc.Description = 'Batchcompute Python SDK'
job_desc.Priority = 100

print(job_desc)

# You can create a new job with this description now!
...
```

* 也可以通过dict或者dict的JSON串批量设置作业的描述信息。

```python
from batchcompute import Jobdescription, Taskdescription, TaskDag, ResourceDescription

job_json = '''{
    "JobName": "find-prime"
    "JobTag": "Batchcompute",
    "Priority": 0, 
    "TaskDag": {
        "TaskDescMap": {
            "Find": {
                "PackageUri": "oss://your-bucket/batch_python_sdk/worker.tar.gz",
                "ProgramName": "find_prime_worker.py",
                "ProgramType": "python",
                "InstanceCount": 1,
                "ResourceDescription": {
                    "Cpu": 800,
                    "Memory": 2000
                },
                "EnvironmentVariables": {},
                "ImageId": "img-xxxx",
                "StdoutRedirectPath": "oss://your-bucket/batch_python_sdk/logs/",
                "StderrRedirectPath": "oss://your-bucket/batch_python_sdk/logs/"
            }
        },
        "Dependencies": {}
    }
}'''

job_desc = JobDescription(job_json)

print job_desc.JobName
print job_desc.JobTag
print job_desc.TaskDag
print job_desc.Description
print job_desc.Priority

print job_desc

```
#### （2） TaskDag类型

**参数说明：**

| 参数 | 类型 | 描述 |
|----------|----------|----------|
| __properties__ | dict, str, TaskDag object | 所有任务的映射以及任务间依赖关系的描述信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1. | __TaskDescMap__ | dict | 所有任务名与任务描述的映射信息 |
| 2. | __Dependencies__ | dict | 所有任务间的依赖关系 |

**方法说明 ：**

| 序号 | 方法 | 描述 |
| :-----: | :----: | ---- |
| 1. | __add_task__ | 增加一个任务 |
| 2. | __get_task__ | 通过任务名获取任务信息 |
| 3. | __delete_task__ | 删除某个任务 |

* 可以通过属性赋值的方式提供任务信息, 如下：

e.g.
```python
# Refer to the TaskDescription class to have a look at how to create a new task.
find_task = ...

task_dag = TaskDag()
task_dag.TaskDescMap = {
    'Find': find_task
}
task_dag.Dependencies = {}
```

* 也可以通过类方法来增加任务信息，如下：

e.g.
```python
# Refer to the TaskDescription class to have a look at how to create a new task.
find_task = ...

task_dag = TaskDag()
task_dag.add_task(task_name='Find', task=find_task)
task_dag.Dependencies = {}
```

#### （3） TaskDescription 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, TaskDescription object | 单个任务的描述信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1.  | __PackageUri__ | str | 用户的可执行程序包路径，应该是一个oss路径。 |
| 2.  | __ProgramName__ | str | 当前task对应的需要执行的用户的主程序名称 |
| 3.  | __ProgramType__ | str | 用户程序的类型， 现阶段仅支持python、php两种，近期将支持java |
| 4.  | __ProgramArguments__ | str | 用户程序的命令行参数 |
| 5.  | __ImageId__ | str | 作业使用的镜像ID，请参考[这里]({{!brief-manual/images!}}) |
| 6.  | __InstanceCount__ | str | 任务中实例的个数，正数 |
| 7.  | __Timeout__ | int | 设置任务中的一个实例的最长执行时间(超时时间)，范围为[1,86400]，单位为秒。 |
| 8.  | __EnvironmentVariables__ | dict | 环境变量 |
| 9.  | __StdoutRedirectPath__ | str | 用户程序标准输出路径 |
| 10. | __StderrRedirectPath__ | str | 用户程序标注出错路径 |
| 11. | __ResourceDescription__ | ResourceDescription object | 任务资源需求描述信息 |
| 12. | __OssMapping__ | dict | NFS挂载功能从OSS存储到本地磁盘的映射关系描述 |
| 13. | __OssMappingLock__ | bool | 布尔型变量，用来确定NFS挂载服务是否支持网络文件锁。如果设置为true，则会开启网络锁服务，为文件锁提供后端支持 |
| 14. | __OssMappingLocale__ | str |  OSS上的Object统一采用UTF-8编码命名，这个参数可以决定挂载后使用的本地字符集。 |

e.g.
```python
find_task = TaskDescription()
# Refer to the ResourceDescription class to have a look at how to create a resource description.
# Default set cpu needs to 800 and memory needs to 2000.
resource = ResourceDescription()

find_task.PackageUri = 'oss://your-bucket/batch-python-sdk/worker.tar.gz'
find_task.ProgramName = 'find_prime_worker.py'
find_task.ProgramType = 'python'
find_task.Priority = 0 
find_task.ImageId = 'img-xxxx'
find_task.InstanceCount = 1
find_task.EnvironmentVariables = {}
find_task.StdoutRedirectPath = 'oss://your-bucket/batch-python-sdk/logs/'
find_task.StderrRedirectPath = 'oss://your-bucket/batch-python-sdk/logs/'
find_task.ResourceDescription = resource

# You can now add this task description to a TaskDag object through its add_task method.
```
#### （4） ResourceDescription 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, ResourceDescription | 资源需求描述信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1. | __Cpu__ | int | 单个实例所耗 CPU，100 对应 1 个 CPU，范围为[800，2400] |
| 2. | __Memory__ | int | 单个实例所需内存，单位 MB，范围为[2000,65536] |

e.g.
```python
resource = ResourceDescription()

resource.Cpu = 16
resource.Memory = 2000

# You can add this description to a task description now.
...
```

### 4.2 get_job_description

**参数说明：**

| 参数 | 类型 | 描述 |
|:------:|:------:|--------|
| __job__ | CreateResponse, str | 作业ID |

**返回值说明：**  
> get_job_description方法返回一个`GetResponse`对象，封装了`JobDescription`对象的所有接口和属性。
> 请参阅上节中`JobDescription`类的描述，了解`JobDescription`对象的属性.

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Job ID.
    job = 'job-xxxx'
    # Get job description, it returns a GetResponse object.
    # You can use job_desc just like a JobDescription object.
    job_desc = client.get_job_description(job)
    print(job_desc.JobName, job_desc.TaskDag, job_desc.Priority)
except ClientError, e:
    print(e)
```

### 4.3 update_job_priority

>当作业的状态为Stopped和Failed才可以调用该接口。

**参数说明：**

| 参数 | 类型 | 描述 |
|:------:|:------:|--------|
| __job__ | CreateResponse object, str | 作业ID |
| __priority__ | int | 作业优先级， [0,1000]范围内的整数指定， 优先级数值越高表示作业调度时的优先级越高 |

**返回值说明：**
> update_job_priority 方法将返回一个 `ActionResponse` 对象, `ActionResponse`仅提供了request ID和状态码两个属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Job ID.
    job = 'job-xxxx'
    new_priority = 200
    # Get run-time infromation of the job.
    job_detail = client.get_job(job)
    if job_detail.State == 'Stopped':
        # Only the priority of a stopped job can be modified.
        client.update_job_priority(job, new_priority)
    job_detail = client.get_job(job)
    assert job_detail.Priority == new_priority
except ClientError, e:
    print(e)
```

### 4.4 stop_job

>当作业的状态为Waiting或Running，才可以调用该接口。

**参数说明：**

| 属性 | 类型 | 描述 |
|:------:|:------:|--------|
| __job__ | CreateResponse, str | 作业ID |

**返回值说明：**
> stop_job方法将返回一个 `ActionResponse` 对象, `ActionResponse`仅提供了request ID和状态码两个属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Job ID.
    job = 'job-xxxx'
    job_detail = client.get_job(job)
    if job_detail.State in ['Waiting', 'Running']:
        # Only running or waiting jobs can be stopped.
        client.stop_job(job)
    job_detail = client.get_job(job)
    assert job_detail.State == 'Stopped'
except ClientError, e:
    print(e)
```

### 4.5 start_job

>当作业的状态为Stopped或者Failed，才可以调用该接口。
* 当 Failed 状态的作业重启之后，已经运行成功的 Instance 不会重新运行。

**参数说明：**

| 属性 | 类型 | 描述 |
|:------:|:------:|--------|
| __job__ | CreateResponse, str | 作业ID |

**返回值说明：**
> start_job方法将返回一个 `ActionResponse` 对象, `ActionResponse`仅提供了request ID和状态码两个属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Job ID.
    job = 'job-xxxx'
    job_detail = client.get_job(job)
    if job_detail.State == 'Stopped':
        # Only stopped job can be restarted.
        client.start_job(job)
    job_detail = client.get_job(job)
    assert job_detail.State in ['Waiting', 'Running']
except ClientError, e:
    print(e)
```

### 4.6 delete_job

>当作业的状态为Stopped，Terminated或Failed，才可以调用该接口。

**参数说明：**

| 属性 | 类型 | 描述 |
|:------:|:------:|--------|
| __job__ | CreateResponse, str | 作业ID |

**返回值说明：**
> delete_job方法将返回一个 `ActionResponse` 对象, `ActionResponse`仅提供了request ID和状态码两个属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Job ID.
    job = 'job-xxxx'
    client.delete_job(job)
except ClientError, e:
    print(e)
```

### 4.7 get_job

**参数说明：**

| 属性 | 类型 | 描述 |
|:------:|:------:|--------|
| __job__ | CreateResponse, str | 作业ID |

**返回值说明：**
> get_job方法返回一个 `GetResponse` 对象,它封装了 `Job` 对象的所有接口和属性 。
> 请参阅`Job`类的描述，了解`Job`对象的属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    job = 'job-xxxx'

    # Get job run-time information, it returns a GetResponse object.
    # You can use job_detail just like a Job object.
    job_detail = client.get_job(job)
    print(job_detail.State)
    ...
except ClientError, e:
    print(e)
```

#### （1） Job 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, TaskDag | 作业的当前状态信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1.  | __JobId__ | str | 作业ID |
| 2.  | __JobName__ | str | 作业名称 |
| 3.  | __Description__ | str| 作业的简要描述 |
| 4.  | __Priority__ | int | 作业优先级 |
| 5.  | __State__ | str | 作业的运行状态 |
| 6.  | __OwnerId__ | int | owner用户账号的阿里云ID |
| 7.  | __CreateTime__ | int | 作业的创建时间，单位：秒 |
| 8.  | __StartTime__ | int | 作业的开始时间，单位：秒， 如果还在Waiting状态，则为0 |
| 9.  | __EndTime__ | int | 作业的结束时间，单位：秒， 如果还没结束，则为0 |
| 10. | __NumTotalTask__ | int | 作业的任务总数 |
| 11. | __NumFinishedTask__ | int | 运行完成的任务总数 |
| 12. | __NumFailedTask__ | int | 运行失败的任务总数 |
| 13. | __NumWaitingTask__ | int | 等待中的任务数 |
| 14. | __NumRunningTask__ | int | 运行中的任务数 |
| 15. | __NumStoppedTask__ | int | 停止的任务数 |
| 16. | __NumTotalInstance__ | int | 作业的实例总数 |
| 17. | __NumFinishedInstance__ |int | 运行完成的实例总数 |
| 18. | __NumFailedInstance__ | int | 运行失败的实例总数 |
| 19. | __NumWaitingInstance__ | int | 等待中的实例总数 |
| 20. | __NumRunningInstance__ | int | 运行中的实例总数 |
| 21. | __NumStoppedInstance__ | int | 停止的实例总数|


### 4.8 list_jobs

**返回值说明：**
> list_jobs方法返回一个 `ListResponse` 对象, 是`Job`对象的集合，可以像使用list对象一样使用它。
> 请参阅上节中Job类的描述，了解Job对象的属性。

e.g.:

```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Get a list of all jobs owned by the user.
    job_list = client.list_job_status()
    for job_detail in job_list:
        print(job_detail.JobId, job_detail.State, job_detail.StartTime)
except ClientError, e:
    print(e)
```

### 4.9 list_tasks

**参数说明：**

| 属性 | 类型 | 描述 |
|:------:|:------:|:--------:|
| __job__ | CreateResponse, str | 作业ID |

**返回值说明：**
> list_tasks方法将返回一个`ListResponse` 对象, 是一个`Task`对象的集合,可以像使用list对象一样使用它。
> 请参阅`Task`类型的描述，了解`Task`对象的属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    # Job ID.
    job = 'job-xxxx'
    indent = ' '*4

    task_list = client.list_tasks(job)
    for task_detail in task_list:
        print(task_detail.TaskName, task_detail.State)
        for instance_detail in task.InstanceStatusList:
            print(instance_detail.InstanceId, instance_detail.State)
except ClientError, e:
    print(e)
```

#### （1） Task 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, Task | 任务的当前状态信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1. | __TaskName__ | str | 任务名称 |
| 2. | __State__ | str | 任务的运行状态 |
| 3. | __StartTime__ | int, str | 任务开始时间，单位：秒，如果还在Waiting状态，则为0 |
| 4. | __EndTime__ | int, str | 任务结束时间， 单位：秒， 如果还没结束，则为0 |
| 5. | __InstanceList__ | list | 任务所包含的实例集合，是Instance对象的集合 |

#### （2） Instance 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, Instance object | 实例状态信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1. | __InstanceId__ | int | 实例ID |
| 2. | __State__ | str | 实例的运行状态 |
| 3. | __StartTime__ | int, str | 实例的开始时间，单位：秒， 如果还在Waiting状态，则为0 |
| 4. | __EndTime__ | int, str | 实例的结束时间，单位：秒， 如果还没结束，则为0 |


### 4.10 list_images

**返回值说明：**
> list_images方法将返回一个`ListResponse`对象, 是一个`Image`对象的集合，可以像使用list对象一个使用它。
> 请参阅`Image`类型的描述，了解`Image`对象的属性。

e.g.
```python
try:
    # Get a Client object.
    client = Client(...
    ...

    image_list = client.list_images()
    for image_detail in image_list:
        print(image_detail.ImageId, image_detail.ImageName)
except ClientError, e:
    print(e)

```

#### （1） Image 类

**参数说明：**

| 参数 | 类型 | 描述 |
|:----------:|:----------:|----------|
| __properties__ | dict, str, Image | 镜像的状态信息 |

**属性说明：**

| 序号 | 属性 | 类型 | 描述 |
| :-----: | :----: | :----: | ---- |
| 1. | __Platform__ | str | 镜像运行环境类型：Windows或者Linux |
| 2. | __ImageId__ | str | 镜像的ID |
| 3. | __ImageName__ | str | 镜像名称 |
| 4. | __Description__ | str | 镜像的简短描述 |

