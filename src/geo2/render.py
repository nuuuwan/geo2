from utils import logx
from utils.xmlx import _
from gig import ents
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
    fill="white",
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

def render(region_to_geo):
    bbox = core.BBOX_LK
    t = get_transform(bbox)
    rendered_polygons = rendered_polygons(t, region_to_geo)
    svg = _(
        'svg',
        rendered_polygons,
        STYLE_SVG,
    )
    return svg

def draw(region_to_geo):
    svg = render(region_to_geo)
    svg_file = '/tmp/geo2.render.svg'
    svg.store(svg_file)
    log.info(f'Wrote {svg_file}')

if __name__ == '__main__':
    from geo import geodata

    regions = ents.get_entities('province')
    region_ids = [region['id'] for region in regions]
    region_to_geo = dict(
        list(
            map(
                lambda region_id: [
                    region_id,
                    geodata.get_region_geo(region_id),
                ],
                region_ids,
            )
        )
    )
    region_to_bbox = dict(
        list(
            map(
                lambda item: [item[0], core.get_bbox(item[1])],
                region_to_geo.items(),
            )
        )
    )
    draw(region_to_geo)
