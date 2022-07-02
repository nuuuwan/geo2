from geo2 import gbox, core, render
from utils import logx, colorx
from utils.xmlx import _
import random

log = logx.get_logger('render_tree')

random.seed(1)
REGION_TO_COLOR = {}
def get_region_color(region_id):
    if region_id not in REGION_TO_COLOR:
        REGION_TO_COLOR[region_id] = colorx.random_hex()
    return REGION_TO_COLOR[region_id]


def render_gbox(t, gbox_k, fill):
    x1, y1 = t(gbox_k.min_lnglat)
    x2, y2 = t(gbox_k.max_lnglat)

    width = x2 - x1
    height = y1 - y2

    return _('rect', None, dict(
        x=x1,
        y=y1,
        width=width,
        height=height,
        fill=fill,
        stroke="black",
        stroke_width=0.1,
    ))

def render_gboxes(t, tree, rendered_gboxes):
    for k, v in tree.items():
        if isinstance(v, str):
            gbox_k = gbox.GBox.from_str(k)
            region_id = v
            color = get_region_color(region_id)
            rendered_gboxes.append(render_gbox(t, gbox_k, color))
        elif isinstance(v, list):
            gbox_k = gbox.GBox.from_str(k)
            rendered_gboxes.append(render_gbox(t, gbox_k, 'gray'))
        else:
            rendered_gboxes = render_gboxes(t, v, rendered_gboxes)

    return rendered_gboxes

def draw_tree(tree):

    bbox = core.BBOX_LK
    log.debug(f'{bbox=}')
    t = render.get_transform(bbox)

    rendered_gboxes = render_gboxes(t, tree, [])


    svg = _(
        'svg',
        [
            render.render_rect(),
        ] + rendered_gboxes,
        render.STYLE_SVG,
    )
    svg_file = '/tmp/geo2.tree.svg'
    svg.store(svg_file)
    log.info(f'Wrote {svg_file}')


if __name__ == '__main__':
    tree = gbox.get_tree()
    draw_tree(tree)
