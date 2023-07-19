
import pandas
import numpy

# ---------------------------------------------------------------

def index_date_filter(df, date_start=None, date_end=None):
    if date_start is not None:
        df = df.loc[df.index >= date_start]
    if date_end is not None:
        df = df.loc[df.index <= date_end]
    return df

def df_min_max(
    df,
    with_cols=None,
    excl_cols=None,
    symmetrical=False,
):
    ks = list(df.columns)
    if with_cols:
        ks = [k for k in ks if k in with_cols]
    if excl_cols:
        ks = [k for k in ks if k not in excl_cols]
    df_vs = df[ks].values
    v_min = numpy.min(df_vs)
    v_max = numpy.max(df_vs)
    if v_min < 0 and v_max < 0:
        pass
    elif v_min > 0 and v_max > 0:
        pass
    elif not symmetrical:
        pass
    else:
        v_lim = max([abs(v_min), v_max])
        v_min = -1 * v_lim
        v_max = v_lim
    return v_min, v_max

def melt_with_index(df, index_as="index"):
    return pandas.concat([
        df.loc[[v]].melt().assign(
            **{index_as: [v for _ in df.columns]}
        ) for v in df.index
    ])

# ---------------------------------------------------------------
