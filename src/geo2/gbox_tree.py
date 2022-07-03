import json
import os
from functools import cache, cached_property

from utils import JSONFile, logx

from geo2 import gbox, regionx

log = logx.get_logger('geo2.gbox_tree')


def build(region_entity_type, log_inv_min_prec):
    min_prec = 0.1 ** log_inv_min_prec
    region_to_geo = regionx.get_region_to_geo(region_entity_type)
    root = gbox.GBox.root()
    return root.get_tree(region_to_geo, min_prec)


def store(tree_file, tree):
    JSONFile(tree_file).write(tree)
    n_tree_file = os.path.getsize(tree_file) / 1_000_000
    log.info(f'Wrote {tree_file} ({n_tree_file:.2f}MB)')
    os.system(f'open -a atom {tree_file}')


def load(tree_file):
    if not os.path.exists(tree_file):
        return None
    return JSONFile(tree_file).read()


def find_regions(tree, lnglat):
    for k, v in tree.items():
        gbox_k = gbox.GBox.from_str(k)
        log.debug(f'{gbox_k=}')
        if gbox_k.contains_lnglat(lnglat):
            if isinstance(v, str):
                return [v]
            if isinstance(v, list):
                return v
            return find_regions(v, lnglat)
    return []


class GBoxTree:
    def __init__(self, region_entity_type, log_inv_min_prec):
        self.region_entity_type = region_entity_type
        self.log_inv_min_prec = log_inv_min_prec

        self.tree = load(self.tree_file)
        if not self.tree:
            self.tree = self.build(
                self.region_entity_type, self.log_inv_min_prec
            )
            self.store(self.tree_file, self.tree)

    @cache
    def __len__(self):
        return len(json.dumps(self.tree))

    @cached_property
    def tree_file(self):
        return (
            f'/tmp/geo2.tree.{self.region_entity_type}'
            + f'.prec{self.log_inv_min_prec}.json'
        )

    def __str__(self):
        n_m = len(self) / 1_000_000
        return (
            f'GBoxTree({self.region_entity_type=}, '
            + f'{self.log_inv_min_prec=}, size={n_m:.2f}MB)'
        )

    def find_regions(self, lnglat):
        return find_regions(self.tree, lnglat)
