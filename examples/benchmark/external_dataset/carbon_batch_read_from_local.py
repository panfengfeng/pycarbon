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

###
# Adapted to pycarbon dataset using original contents from
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/tutorials/mnist/mnist_softmax.py
###

from __future__ import division, print_function

import time
import argparse

import jnius_config

from pycarbon.core.carbon_reader import make_batch_carbon_reader

from pycarbon.reader import make_reader

from examples import DEFAULT_CARBONSDK_PATH
from examples.benchmark.external_dataset.generate_benchmark_external_dataset import ROW_COUNT


def just_read_batch(dataset_url='file:///tmp/benchmark_external_dataset', num_epochs=1):
  with make_batch_carbon_reader(dataset_url, num_epochs=num_epochs) as train_reader:
    i = 0
    start = time.time()
    for schema_view in train_reader:
      for j in range(len(schema_view.id)):
        print(schema_view.id[j])
        i += 1
        if i % ROW_COUNT == 0:
          end = time.time()
          print("time is " + str(end - start))
          start = end
    assert i == ROW_COUNT * num_epochs
    return i


def just_unified_read_batch(dataset_url='file:///tmp/benchmark_external_dataset', num_epochs=1):
  with make_reader(dataset_url, num_epochs=num_epochs) as train_reader:
    i = 0
    start = time.time()
    for schema_view in train_reader:
      for j in range(len(schema_view.id)):
        print(schema_view.id[j])
        i += 1
        if i % ROW_COUNT == 0:
          end = time.time()
          print("time is " + str(end - start))
          start = end
    assert i == ROW_COUNT * num_epochs
    return i


def main():
  parser = argparse.ArgumentParser(description='Tensorflow hello world')
  parser.add_argument('-c', '--carbon-sdk-path', type=str, default=DEFAULT_CARBONSDK_PATH,
                      help='carbon sdk path')

  args = parser.parse_args()

  jnius_config.set_classpath(args.carbon_sdk_path)

  jnius_config.add_options('-Xrs', '-Xmx6096m')
  # jnius_config.add_options('-Xrs', '-Xmx6096m', '-agentlib:jdwp=transport=dt_socket,server=y,suspend=y,address=5555')
  print("Start")
  start = time.time()

  just_read_batch()

  just_unified_read_batch()

  end = time.time()
  print("all time: " + str(end - start))
  print("Finish")


if __name__ == '__main__':
  main()
