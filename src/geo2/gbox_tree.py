import os

from utils import JSONFile, logx

from geo2 import gbox, regionx

log = logx.get_logger('geo2.gbox_tree')

def get_tree_file(region_entity_type, log_inv_min_prec):
    return f'/tmp/geo2.tree.{region_entity_type}.prec{log_inv_min_prec}.json'


def store_tree(region_entity_type, log_inv_min_prec):
    log.debug(f'{region_entity_type=}, {log_inv_min_prec=}')
    min_prec = 0.1 ** log_inv_min_prec
    region_to_geo = regionx.get_region_to_geo(region_entity_type)
    root = gbox.GBox.root()
    tree = root.get_tree(region_to_geo, min_prec)

    tree_file = get_tree_file(region_entity_type, log_inv_min_prec)
    JSONFile(tree_file).write(tree)
    n_tree_file = os.path.getsize(tree_file) / 1_000_000
    log.info(f'Wrote {tree_file} ({n_tree_file:.2f}MB)')
    os.system(f'open -a atom {tree_file}')
    return tree

def load_tree(region_entity_type, log_inv_min_prec):
    tree_file = get_tree_file(region_entity_type, log_inv_min_prec)
    if not os.path.exists(tree_file):
        store_tree(region_entity_type, log_inv_min_prec)

    return JSONFile(tree_file).read()

if __name__ == '__main__':
    store_tree('province', 1)
