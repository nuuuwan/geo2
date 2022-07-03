import os

from utils import logx
from utils.xmlx import _

from geo2 import core

WIDTH = 500
HEIGHT = 500
log = logx.get_logger('render')

STYLE_SVG = dict(
    width=WIDTH,
    height=HEIGHT,
)

STYLE_RECT = dict(
    width=WIDTH,
    height=HEIGHT,
    x=0,
    y=0,
    fill="#eee",
    stroke="black",
)

STYLE_POLYGON = dict(
    fill="white",
    fill_opacity=0.1,
    stroke="black",
)


def get_transform(norm_bbox):
    [min_lng, max_lng, min_lat, max_lat] = norm_bbox
    lng_span, lat_span = max_lng - min_lng, max_lat - min_lat

    width, height = WIDTH, HEIGHT
    r = lng_span / lat_span
    if r > 1:
        height /= r
    else:
        width *= r

    padding_x = (WIDTH - width) / 2
    padding_y = (HEIGHT - height) / 2

    def t(lnglat):
        lng, lat = lnglat
        px = (lng - min_lng) / lng_span
        py = (lat - min_lat) / lat_span

        return padding_x + px * width, padding_y + (1 - py) * height

    return t


def render_polygon(t, polygon):
    d_list = []
    cmd = 'M'
    for lnglat in polygon:
        x, y = t(lnglat)
        d_list.append(f'{cmd}{x:.0f},{y:.0f}')
        cmd = 'L'
    d = ''.join(d_list) + 'Z'
    return _('path', [], {'d': d} | STYLE_POLYGON)


def render_rect():
    return _('rect', None, STYLE_RECT)


def render_polygons(t, region_to_geo):
    rendered_polygons = []
    for region_id, geo in region_to_geo.items():
        for polygon in core.iter_polygons(geo):
            rendered_polygons.append(render_polygon(t, polygon))
    return rendered_polygons


def render_svg(region_to_geo):
    bbox = core.BBOX_LK
    t = get_transform(bbox)
    rendered_polygons = render_polygons(t, region_to_geo)
    svg = _(
        'svg',
        rendered_polygons,
        STYLE_SVG,
    )
    return svg


def draw(region_to_geo):
    svg = render_svg(region_to_geo)
    svg_file = '/tmp/geo2.render.svg'
    svg.store(svg_file)
    log.info(f'Wrote {svg_file}')
    os.system(f'open -a firefox {svg_file}')


if __name__ == '__main__':
    from geo2 import regionx

    region_to_geo = regionx.get_region_to_geo()
    draw(region_to_geo)
