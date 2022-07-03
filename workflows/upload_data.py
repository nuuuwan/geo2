import os

from utils import File, logx, timex

from geo2 import common, gbox_tree, render_tree

log = logx.get_logger('geo2.workflows.upload_data')


def build_readme():
    time_id = timex.get_time_id()
    lines = [
        '# Geo2',
        '*Various geospatial utilities*',
        '---',
        f'Last updated at **{time_id}**',
    ]
    readme_file = os.path.join(common.DIR_DATA, 'README.md')
    File(readme_file).write('\n\n'.join(lines))
    log.info(f'Wrote {readme_file}')


def upload_data():
    common.init_dir_data()

    for region_entity_type, log_inv_min_prec0 in [
        ['province', 2],
        ['district', 3],
        ['dsd', 3],
    ]:
        for i in range(0, log_inv_min_prec0):
            log_inv_min_prec = i + 1
            gbox_tree.GBoxTree(region_entity_type, log_inv_min_prec)
            render_tree.draw_tree(region_entity_type, log_inv_min_prec)

    build_readme()


if __name__ == '__main__':
    upload_data()
