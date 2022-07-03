import os
from functools import cached_property

from utils import JSONFile, logx

from geo2 import core, gbox_base

log = logx.get_logger('geo2.gbox')

MIN_PREC = 0.9 / 16
SPLITS = 2


class GBox(gbox_base.GBoxBase):
    def contains_lnglat(self, lnglat):
        lng, lat = lnglat
        return all(
            [
                self.min_lng < lng,
                lng < self.max_lng,
                self.min_lat < lat,
                lat < self.max_lat,
            ]
        )

    def within_geo(self, geo):
        [min_lng, max_lng, min_lat, max_lat] = core.get_bbox(geo)
        return all(
            [
                min_lng < self.min_lng,
                self.max_lng < max_lng,
                min_lat < self.min_lat,
                self.max_lat < max_lat,
            ]
        )

    def overlaps_with_geo(self, geo):
        for lnglat in core.iter_lnglat(geo):
            if self.contains_lnglat(lnglat):
                return True
        return False

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

    def get_tree(self, region_to_geo):
        print('[get_tree] ' + str(self), end="\r")
        filtered_region_to_geo = dict(
            list(
                filter(
                    lambda item: self.overlaps_with_geo(item[1]),
                    region_to_geo.items(),
                )
            )
        )

        # n_filtered_region_to_geo = len(filtered_region_to_geo)
        # if n_filtered_region_to_geo == 0:
        #     filtered_region_to_geo = dict(
        #         list(
        #             filter(
        #                 lambda item: self.within_geo(item[1]),
        #                 region_to_geo.items(),
        #             )
        #         )
        #     )

        filtered_region_ids = list(filtered_region_to_geo.keys())
        n_filtered_region_ids = len(filtered_region_ids)

        if n_filtered_region_ids == 0:
            return None

        if n_filtered_region_ids == 1:
            return filtered_region_ids[0]

        if self.prec <= MIN_PREC:
            return filtered_region_ids

        tree = {}
        for child_gbox in self.child_list:
            child_tree = child_gbox.get_tree(filtered_region_to_geo)
            if child_tree:
                tree[str(child_gbox)] = child_tree
        return tree

    @staticmethod
    def root():
        return GBox([0, 0], 1)


def store_tree_file(region_to_geo):
    root = GBox.root()
    tree = root.get_tree(region_to_geo)
    tree_file = '/tmp/geo2.tree.json'
    JSONFile(tree_file).write(tree)
    n_tree_file = os.path.getsize(tree_file) / 1_000_000
    log.info(f'Wrote {tree_file} ({n_tree_file:.2f}MB)')
    os.system(f'open -a atom {tree_file}')
    return tree


if __name__ == '__main__':
    from geo2 import regionx

    region_to_geo = regionx.get_region_to_geo()
    store_tree_file(region_to_geo)
