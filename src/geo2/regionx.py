from functools import cache

from geo import geodata
from gig import ents
from utils import logx

from geo2 import core

log = logx.get_logger('render')
REGION_ENTITY_TYPE = 'province'


@cache
def get_regions():
    return ents.get_entities(REGION_ENTITY_TYPE)


@cache
def get_region_ids():
    regions = get_regions()
    return [region['id'] for region in regions]


@cache
def get_region_to_geo():
    region_ids = get_region_ids()
    return dict(
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


@cache
def get_region_to_bbox():
    region_to_geo = get_region_to_geo()
    return dict(
        list(
            map(
                lambda item: [item[0], core.get_bbox(item[1])],
                region_to_geo.items(),
            )
        )
    )
