from functools import cache

from geo import geodata
from gig import ents
from utils import logx

log = logx.get_logger('render')


@cache
def get_regions(region_entity_type):
    return ents.get_entities(region_entity_type)


@cache
def get_region_ids(region_entity_type):
    regions = get_regions(region_entity_type)
    return [region['id'] for region in regions]


@cache
def get_region_to_geo(region_entity_type):
    region_ids = get_region_ids(region_entity_type)
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
