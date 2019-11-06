
import modin.pandas as pd


class GenomicFile(object):
    dataframe_lib = pd

    @classmethod
    def read(cls, *args, **kwargs):
        df = cls._read(*args, **kwargs)
        df._tahoe_parse = cls._parse(df)
        df._tahoe_to_json = cls._to_json(df)
        df._pileup_visualization = cls._visualization(df)
        return df

    @classmethod
    def _read(cls, *args, **kwargs):
        raise NotImplementedError("Must be implemented in children classes")

    @classmethod
    def _parse(cls, df):
        raise NotImplementedError("Must be implemented in children classes")

    @classmethod
    def _to_json(cls, df):
        raise NotImplementedError("Must be implemented in children classes")
    @classmethod
    def _visualization(cls, df):
        raise NotImplementedError("Must be implemented in children classes")

    @classmethod
    def from_pandas(cls, df):
        df._tahoe_parse = cls._parse(df)
        df._tahoe_to_json = cls._to_json(df)
        return df
