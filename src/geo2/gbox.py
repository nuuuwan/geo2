import os
from functools import cached_property

from geo import geodata
from gig import ents
from utils import JSONFile, logx

from geo2 import core

log = logx.get_logger('geo2.gbox')

MIN_PREC = 0.01
SPLITS = 2


LATLNG0 = [79, 5]
SPAN0 = 5


class GBox:
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

    def __str__(self):
        return f'{self.ix}:{self.iy}:{self.n}'

    def to_str(self):
        return str(self)

    @staticmethod
    def from_str(s):
        [ix, iy, n] = [(int)(si) for si in s.split(':')]
        return GBox([ix, iy], n)

    def contains_bbox(self, bbox):
        min_lng, max_lng, min_lat, max_lat = bbox

        return all(
            [
                self.min_lng < max_lng,
                min_lng < self.max_lng,

                self.min_lat < max_lat,
                min_lat < self.max_lat,
            ]
        )

    @cached_property
    def child_list(self):
        child_gbox_list = []
        child_n = self.n * SPLITS
        for qx in range(0, SPLITS):
            for qy in range(0, SPLITS):
                child_gbox_list.append(
                    GBox(
                        [
                            self.ix * SPLITS + qx,
                            self.iy * SPLITS + qy,
                        ],
                        child_n,
                    )
                )
        return child_gbox_list

    def get_tree(self, region_to_bbox):
        contained_region_to_bbox = dict(
            list(
                filter(
                    lambda item: self.contains_bbox(item[1]),
                    region_to_bbox.items(),
                )
            )
        )

        contained_region_ids = list(contained_region_to_bbox.keys())
        n_contained_region_ids = len(contained_region_ids)

        if n_contained_region_ids == 0:
            return None

        if n_contained_region_ids == 1:
            return contained_region_ids[0]

        if self.prec <= MIN_PREC:
            return contained_region_ids

        tree = {}
        for child_gbox in self.child_list:
            child_tree = child_gbox.get_tree(contained_region_to_bbox)
            if child_tree:
                tree[str(child_gbox)] = child_tree
        return tree

    @staticmethod
    def root():
        return GBox([0, 0], 1)


def get_tree(region_to_bbox, force=True):
    tree_file = '/tmp/geo2.tree.json'
    if os.path.exists(tree_file) and not force:
        return JSONFile(tree_file).read()

    root = GBox.root()
    tree = root.get_tree(region_to_bbox)

    tree_file = '/tmp/geo2.tree.json'
    JSONFile(tree_file).write(tree)
    n_tree_file = os.path.getsize(tree_file) / 1_000_000
    log.info(f'Wrote {tree_file} ({n_tree_file:.2f}MB)')
    return tree
