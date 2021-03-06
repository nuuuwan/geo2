import random

from utils import colorx, logx
from utils.xmlx import _

from geo2 import core, gbox, gbox_tree, regionx, render

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

    return _(
        'rect',
        None,
        dict(
            x=x1,
            y=y2,
            width=width,
            height=height,
            fill=fill,
            fill_opacity=0.5,
            stroke="black",
            stroke_width=0.1,
        ),
    )


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


def render_svg(region_to_geo, tree):
    bbox = core.BBOX_LK
    t = render.get_transform(bbox)

    rendered_polygons = render.render_polygons(t, region_to_geo)
    rendered_gboxes = render_gboxes(t, tree, [])

    return _(
        'svg',
        [
            render.render_rect(),
        ]
        + rendered_gboxes
        + rendered_polygons,
        render.STYLE_SVG,
    )


def draw_tree(region_entity_type, log_inv_min_prec):
    region_to_geo = regionx.get_region_to_geo(region_entity_type)
    tree = gbox_tree.GBoxTree(region_entity_type, log_inv_min_prec)

    svg = render_svg(region_to_geo, tree.tree)
    svg_file = tree.tree_file[:-5] + ".svg"
    svg.store(svg_file)
    log.info(f'Wrote {svg_file}')


if __name__ == '__main__':
    draw_tree('province', 1)
