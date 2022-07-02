import math

BBOX_LK = [79, 82, 5, 10]


def get_bbox(geo):
    min_lng, max_lng, min_lat, max_lat = 180, -180, 180, -180
    for lnglat in iter_lnglat(geo):
        lng, lat = lnglat
        min_lng = min(lng, min_lng)
        max_lng = max(lng, max_lng)
        min_lat = min(lat, min_lat)
        max_lat = max(lat, max_lat)
    return [min_lng, max_lng, min_lat, max_lat]


def iter_polygons(geo):
    coordinates = geo['coordinates']
    for polygons in coordinates:
        for polygon in polygons:
            yield polygon


def iter_lnglat(geo):
    for polygon in iter_polygons(geo):
        for lnglat in polygon:
            yield lnglat


def get_prec(digits):
    return 0.1 ** digits


def get_norm_bbox(bbox, digits=0):
    prec = get_prec(digits)
    min_lng, max_lng, min_lat, max_lat = bbox
    min_lng = math.floor(min_lng / prec) * prec
    max_lng = math.ceil(max_lng / prec) * prec

    min_lat = math.floor(min_lat / prec) * prec
    max_lat = math.ceil(max_lat / prec) * prec

    return [min_lng, max_lng, min_lat, max_lat]
