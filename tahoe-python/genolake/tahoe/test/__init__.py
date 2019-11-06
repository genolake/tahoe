
import os
import sys
import tempfile
import unittest


from pyspark.sql import SparkSession

class SparkTestCase(unittest.TestCase):


    def resourceFile(self, file):

        tahoeRoot = os.path.dirname(os.getcwd())
        return os.path.join(os.path.join(tahoeRoot, "tahoe-core/src/test/resources"), file)


    def exampleFile(self, file):

        tahoeRoot = os.path.dirname(os.getcwd())
        return os.path.join(os.path.join(tahoeRoot, "example-files"), file)


    def tmpFile(self):

        tempFile = tempfile.NamedTemporaryFile(delete=True)
        tempFile.close()
        return tempFile.name


    def checkFiles(self, file1, file2):

        f1 = open(file1)
        f2 = open(file2)

        try:
            self.assertEquals(f1.read(), f2.read())
        finally:
            f1.close()
            f2.close()


    def setUp(self):
        self._old_sys_path = list(sys.path)
        class_name = self.__class__.__name__
        self.ss = SparkSession.builder.master('local[4]').appName(class_name).getOrCreate()
        self.sc = self.ss.sparkContext


    def tearDown(self):
        self.ss.stop()
        sys.path = self._old_sys_path
