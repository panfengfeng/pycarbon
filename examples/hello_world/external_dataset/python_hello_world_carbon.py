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

"""Minimal example of how to read samples from a dataset generated by `generate_external_dataset_carbon.py`
using plain Python"""

from __future__ import print_function

import argparse
import jnius_config

from pycarbon.core.carbon_reader import make_batch_carbon_reader

from pycarbon.reader import make_reader

from examples import DEFAULT_CARBONSDK_PATH


def python_hello_world(dataset_url='file:///tmp/carbon_external_dataset'):
  # Reading data from the non-Pycarbon Carbon via pure Python
  with make_batch_carbon_reader(dataset_url, schema_fields=["id", "value1", "value2"]) as reader:
    for schema_view in reader:
      # make_batch_reader() returns batches of rows instead of individual rows
      print("Batched read:\nid: {0} value1: {1} value2: {2}".format(
        schema_view.id, schema_view.value1, schema_view.value2))

  with make_reader(dataset_url, schema_fields=["id", "value1", "value2"]) as reader:
    for schema_view in reader:
      # make_batch_reader() returns batches of rows instead of individual rows
      print("Batched read:\nid: {0} value1: {1} value2: {2}".format(
        schema_view.id, schema_view.value1, schema_view.value2))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Python hello world')
  parser.add_argument('-c', '--carbon-sdk-path', type=str, default=DEFAULT_CARBONSDK_PATH,
                      help='carbon sdk path')

  args = parser.parse_args()

  jnius_config.set_classpath(args.carbon_sdk_path)

  python_hello_world()
