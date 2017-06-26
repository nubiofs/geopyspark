import os
import sys
import numpy as np
import pytest
import unittest

from geopyspark.geotrellis import Tile
from geopyspark.geotrellis.layer import RasterLayer
from geopyspark.geotrellis.constants import SPATIAL
from geopyspark.tests.base_test_class import BaseTestClass
from pyspark.storagelevel import StorageLevel

class LayerWrapperTest(BaseTestClass):
    @pytest.fixture(autouse=True)
    def tearDown(self):
        yield
        BaseTestClass.pysc._gateway.close()

    def test_persist(self):
        arr = np.array([[[1, 1, 1, 1]],
                        [[2, 2, 2, 2]],
                        [[3, 3, 3, 3]],
                        [[4, 4, 4, 4]]], dtype=int)
        tile = Tile(arr, 'INT', -500)

        rdd = BaseTestClass.pysc.parallelize([(self.projected_extent, tile)])
        raster_rdd = RasterLayer.from_numpy_rdd(BaseTestClass.pysc, SPATIAL, rdd)

        self.assertEqual(raster_rdd.is_cached, False)

        raster_rdd.persist(StorageLevel.MEMORY_ONLY)
        self.assertEqual(raster_rdd.is_cached, True)

        raster_rdd.unpersist()
        self.assertEqual(raster_rdd.is_cached, False)

if __name__ == "__main__":
    unittest.main()
