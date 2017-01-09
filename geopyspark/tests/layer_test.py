#!/bin/env python3

import sys

from pyspark import SparkConf, SparkContext, RDD
from pyspark.serializers import AutoBatchedSerializer
from geopyspark.avroserializer import AvroSerializer


if __name__ == "__main__":
    if len(sys.argv) > 3:
        uri = sys.argv[1]
        layer_name = sys.argv[2]
        layer_zoom = int(sys.argv[3])
    else:
        exit(-1)

    sc = SparkContext(appName="layer-test")

    store_factory = sc._gateway.jvm.geopyspark.geotrellis.io.AttributeStoreFactory
    store = store_factory.build("hdfs", uri, sc._jsc.sc())
    header = store.header(layer_name, layer_zoom)
    cell_type = store.cellType(layer_name, layer_zoom)

    reader_factory = sc._gateway.jvm.geopyspark.geotrellis.io.LayerReaderFactory
    reader = reader_factory.build("hdfs", uri, sc._jsc.sc())
    tup = reader.query(layer_name, layer_zoom)
    (jrdd, schema) = (tup._1(), tup._2())
    serializer = AvroSerializer(schema)
    rdd = RDD(jrdd, sc, AutoBatchedSerializer(serializer))
    print(rdd.take(1))
