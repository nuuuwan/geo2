from utils import logx
from utils.xmlx import _

from geo2 import base, core

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
    fill="yellow",
    stroke="red",
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


def render_bbox(t, bbox):
    [min_lng, max_lng, min_lat, max_lat] = bbox
    x1, y1 = t([min_lng, max_lat])
    x2, y2 = t([max_lng, min_lat])
    width = x2 - x1
    height = y2 - y1
    return _(
        'rect',
        None,
        dict(
            x=x1,
            y=y1,
            width=width,
            height=height,
            fill="#ddd",
            stroke="#888",
        ),
    )


def render_squares(t, norm_bbox, digits):
    prec = core.get_prec(digits)
    [min_lng, max_lng, min_lat, max_lat] = norm_bbox
    rendered_squares = []
    for lng in base.rangef(min_lng, max_lng, prec):
        for lat in base.rangef(min_lat, max_lat, prec):
            x1, y1 = t([lng, lat + prec])
            x2, y2 = t([lng + prec, lat])
            width, height = x2 - x1, y2 - y1
            rendered_squares.append(
                _(
                    'rect',
                    None,
                    dict(
                        x=x1,
                        y=y1,
                        width=width,
                        height=height,
                        fill="None",
                        stroke="blue",
                    ),
                )
            )
    return rendered_squares

def render_rect():
    return _('rect', None, STYLE_RECT)

def draw_geo(geo, digits):
    bbox = core.get_bbox(geo)
    log.debug(f'{bbox=}')
    norm_bbox = core.get_norm_bbox(bbox, digits)
    log.debug(f'{norm_bbox=}')
    t = get_transform(norm_bbox)

    rect = render_rect()

    rendered_polygons = []
    for polygon in core.iter_polygons(geo):
        rendered_polygons.append(render_polygon(t, polygon))

    rendered_squares = render_squares(t, norm_bbox, digits)

    svg = _(
        'svg',
        [rect, render_bbox(t, bbox)] + rendered_polygons + rendered_squares,
        STYLE_SVG,
    )
    svg_file = '/tmp/geo2.svg'
    svg.store(svg_file)
    log.info(f'Wrote {svg_file}')


if __name__ == '__main__':
    from geo import geodata

    region_id = 'LK-3'
    region_geo = geodata.get_region_geo(region_id)
    draw_geo(region_geo, 0)
