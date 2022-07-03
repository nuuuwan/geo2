import os

from utils import File, logx, timex

from geo2 import common, gbox_tree

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
    gbox_tree.GBoxTree('province', 2)
    gbox_tree.GBoxTree('district', 3)
    # gbox_tree.GBoxTree('dsd', 4)
    build_readme()


if __name__ == '__main__':
    upload_data()
