#  Copyright (c) 2018-2019 Huawei Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

curdir = os.path.dirname(os.path.realpath(__file__))

jardir = os.path.abspath(os.path.join(curdir, os.path.pardir, os.path.pardir))

DEFAULT_CARBONSDK_PATH = os.path.join(jardir, 'jars/carbondata-sdk.jar')

S3_DATA_PATH = 's3a://sdk/binary'
S3_DATA_PATH1 = 's3a://sdk/binary/sub1'
S3_DATA_PATH2 = 's3a://sdk/binary/sub2'

EXAMPLES_MANIFEST_PATH = os.path.join(jardir, 'examples/data/')

LOCAL_DATA_PATH = os.path.join(jardir, 'examples/data/binary')

IMAGE_DATA_PATH = os.path.join(jardir, 'examples/data/image')
