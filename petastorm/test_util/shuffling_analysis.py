#  Copyright (c) 2017-2018 Uber Technologies, Inc.
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
from __future__ import division

from functools import partial

import numpy as np
from pyspark.sql.types import LongType

from petastorm import make_reader
from petastorm.codecs import ScalarCodec
from petastorm.etl.dataset_metadata import materialize_dataset
from petastorm.unischema import Unischema, UnischemaField, dict_to_spark_row

_ShuffleAnalysisSchema = Unischema('_ShuffleAnalysisSchema',
                                   [UnischemaField('id', np.int64, (), ScalarCodec(LongType()), False)])


def generate_shuffle_analysis_dataset(spark, output_dataset_url, num_rows=1000, row_group_size=100):
    """
    Generates a small dataset useful for doing analysis on shuffling algorithms

    :param spark: spark session
    :param output_dataset_url: location to write dataset
    :param num_rows: how many rows should the dataset include
    :param row_group_size: how many rows in each row group (there is a minimum of 5)
    :return:
    """
    spark_context = spark.sparkContext
    with materialize_dataset(spark, output_dataset_url, _ShuffleAnalysisSchema):
        rows_rdd = spark_context.parallelize(range(num_rows), numSlices=50) \
            .map(lambda i: {'id': i}) \
            .map(partial(dict_to_spark_row, _ShuffleAnalysisSchema))
        spark.createDataFrame(rows_rdd, _ShuffleAnalysisSchema.as_spark_schema()) \
            .sort('id') \
            .coalesce(max(1, int(num_rows / row_group_size))) \
            .write.option('compression', 'none') \
            .parquet(output_dataset_url)


def compute_correlation_distribution(dataset_url,
                                     id_column,
                                     shuffle_row_drop_partitions,
                                     num_corr_samples=100):
    """
    Compute the correlation distribution of a given shuffle_options on an existing dataset.
    Use this to compare 2 different shuffling options compare.
    It is encouraged to use a dataset generated by generate_shuffle_analysis_dataset for this analysis.

    :param dataset_url: Dataset url to compute correlation distribution of
    :param id_column: Column where an integer or string id can be found
    :param shuffle_row_drop_partitions: shuffle_row_drop_partitions to test correlation against
    :param num_corr_samples: How many samples of the correlation to take to compute distribution
    :return: (mean, standard deviation) of computed distribution
    """

    # Read the dataset without any shuffling in order (need to use a dummy pool for this).
    with make_reader(dataset_url,
                     shuffle_row_groups=False,
                     reader_pool_type='dummy') as reader:
        unshuffled = [row[id_column] for row in reader]

    correlations = []
    for _ in range(num_corr_samples):
        with make_reader(dataset_url,
                         shuffle_row_groups=True,
                         shuffle_row_drop_partitions=shuffle_row_drop_partitions) as reader:
            shuffled = [row[id_column] for row in reader]
            correlations.append(abs(np.corrcoef(unshuffled, shuffled)[0, 1]))

    mean = np.mean(correlations)
    std_dev = np.std(correlations)

    return mean, std_dev