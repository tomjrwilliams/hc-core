
import numpy
import pandas
import scipy.stats

def gaussian_kde_1d(x, clip_quantile=None):
    if clip_quantile is None:
        pass
    else:
        if isinstance(clip_quantile, tuple):
            lq, rq = clip_quantile
        else:
            lq = clip_quantile
            rq = 1 - lq
        l = numpy.quantile(x, lq)
        r = numpy.quantile(x, rq)
        x = numpy.clip(x, l, r)

    xmin = x.min()
    xmax = x.max()

    X = numpy.mgrid[xmin:xmax:100j]
    positions = X.ravel()
    kernel = scipy.stats.gaussian_kde(x)
    Z = numpy.reshape(kernel(positions).T, X.shape)
    # z is density over the grid (xmin, xmax)
    return positions, Z

def gaussian_kde_1d_df(xs, **kde_kwargs):
    keys = []
    positions = []
    densities = []
    for key, x in xs.items():
        ps, ds = gaussian_kde_1d(x, **kde_kwargs)
        positions.extend(ps)
        densities.extend(ds)
        keys.extend([key for _ in ds])
    return pandas.DataFrame({
        "key": keys,
        "position": positions,
        "density": densities,
    })

def gaussian_kde_2d(x, y):
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()

    X, Y = numpy.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = numpy.vstack([X.ravel(), Y.ravel()])
    values = numpy.vstack([x, y])
    kernel = scipy.stats.gaussian_kde(values)
    Z = numpy.reshape(kernel(positions).T, X.shape)
    # z is density over the grid ((xmin, xmax) (ymin, ymax))
    return positions, Z