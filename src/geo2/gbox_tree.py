import os

from utils import JSONFile, logx

from geo2 import gbox, regionx

log = logx.get_logger('geo2.gbox_tree')


def store_tree_file(region_entity_type):
    log.debug(f'{region_entity_type=}')
    region_to_geo = regionx.get_region_to_geo(region_entity_type)
    root = gbox.GBox.root()
    tree = root.get_tree(region_to_geo)

    tree_file = f'/tmp/geo2.tree.{region_entity_type}.json'
    JSONFile(tree_file).write(tree)
    n_tree_file = os.path.getsize(tree_file) / 1_000_000
    log.info(f'Wrote {tree_file} ({n_tree_file:.2f}MB)')
    os.system(f'open -a atom {tree_file}')
    return tree


if __name__ == '__main__':
    store_tree_file('province')
