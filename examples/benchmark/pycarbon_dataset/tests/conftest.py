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

from examples import DEFAULT_CARBONSDK_PATH


def pytest_addoption(parser):
  parser.addoption('--pyspark-python', type=str, default=None,
                   help='pyspark python env variable')
  parser.addoption('--pyspark-driver-python', type=str, default=None,
                   help='pyspark driver python env variable')
  parser.addoption('--carbon-sdk-path', type=str, default=DEFAULT_CARBONSDK_PATH,
                   help='carbon sdk path')
  parser.addoption('--access_key', type=str, default=None, required=True,
                   help='access_key of obs')
  parser.addoption('--secret_key', type=str, default=None, required=True,
                   help='secret_key of obs')
  parser.addoption('--end_point', type=str, default=None, required=True,
                   help='end_point of obs')
