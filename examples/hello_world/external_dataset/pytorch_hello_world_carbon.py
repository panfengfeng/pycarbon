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
using pytorch, using make_batch_carbon_reader() instead of make_carbon_reader()"""

from __future__ import print_function

import argparse
import jnius_config

from petastorm.pytorch import DataLoader

from pycarbon.core.carbon_reader import make_batch_carbon_reader

from pycarbon.reader import make_reader
from pycarbon.reader import make_data_loader

from examples import DEFAULT_CARBONSDK_PATH


def pytorch_hello_world(dataset_url='file:///tmp/carbon_external_dataset'):
  with DataLoader(make_batch_carbon_reader(dataset_url)) as train_loader:
    sample = next(iter(train_loader))
    # Because we are using make_batch_reader(), each read returns a batch of rows instead of a single row
    print("id batch: {0}".format(sample['id']))

  with make_data_loader(make_reader(dataset_url)) as train_loader:
    sample = next(iter(train_loader))
    # Because we are using make_batch_reader(), each read returns a batch of rows instead of a single row
    print("id batch: {0}".format(sample['id']))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Pytorch hello world')
  parser.add_argument('-c', '--carbon-sdk-path', type=str, default=DEFAULT_CARBONSDK_PATH,
                      help='carbon sdk path')

  args = parser.parse_args()

  jnius_config.set_classpath(args.carbon_sdk_path)

  pytorch_hello_world()
