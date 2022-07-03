from functools import cache, cached_property

LATLNG0 = [79, 5]
SPAN0 = 5


class GBoxBase:
    def __init__(self, ixiy, n):
        self.ixiy = ixiy
        self.n = n

    @cached_property
    def lng0(self):
        return LATLNG0[0]

    @cached_property
    def lat0(self):
        return LATLNG0[1]

    @cached_property
    def ix(self):
        return self.ixiy[0]

    @cached_property
    def iy(self):
        return self.ixiy[1]

    @cached_property
    def prec(self):
        return 1.0 * SPAN0 / self.n

    @cached_property
    def dlng(self):
        return self.ix * self.prec

    @cached_property
    def dlat(self):
        return self.iy * self.prec

    @cached_property
    def min_lng(self):
        return self.lng0 + self.dlng

    @cached_property
    def min_lat(self):
        return self.lat0 + self.dlat

    @cached_property
    def max_lng(self):
        return self.min_lng + self.prec

    @cached_property
    def max_lat(self):
        return self.min_lat + self.prec

    @cached_property
    def min_lnglat(self):
        return [self.min_lng, self.min_lat]

    @cached_property
    def max_lnglat(self):
        return [self.max_lng, self.max_lat]

    @cached_property
    def mid_lng(self):
        return self.min_lng + self.prec / 2

    @cached_property
    def mid_lat(self):
        return self.min_lat + self.prec / 2

    @cached_property
    def mid_lnglat(self):
        return [self.mid_lng, self.mid_lat]

    @cache
    def __str__(self):
        return f'{self.ix}:{self.iy}:{self.n}'

    def to_str(self):
        return str(self)

    @classmethod
    def from_str(cls, s):
        [ix, iy, n] = [(int)(si) for si in s.split(':')]
        return cls([ix, iy], n)
