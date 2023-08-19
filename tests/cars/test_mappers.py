from assertpy import assert_that

from ir_client.cars.mappers import map_car, map_cars
from ir_client.cars.models import Car


def test_map_cars():
    # todo implement test resource default
    html_file = open("test_resources/home.html", "r")
    cars = map_cars(html_file)
    assert_that(cars.cars).is_length(146)
    # TODO test other cars?


def test_map_car():
    car_dict = {
        "hasMultipleDryTireTypes": False,
        "forceNotChrome": False,
        "hasHeadlights": False,
        "maxWeightPenaltyLB": "551.16",
        "skuname": "ARCA+Menards+Chevy%2FGen+4+Cup",
        "defaultimg": "member_images%2Fcars%2Fdefault%2Fid_24",
        "minPowerAdjustPct": "-5.0",
        "freeWithSubscription": False,
        "price": 11.95,
        "lowername": "arca+menards+chevrolet+impala",
        "retired": False,
        "id": 24,
        "forceChrome": False,
        "is_ps_purchasable": True,
        "sku": 10088,
        "forumID": 623,
        "allowWheelColor": True,
        "detailVideo": "null",
        "maxWeightPenaltyKG": "250.0",
        "allowSponsor2": True,
        "priceDisplay": "11.95",
        "allowSponsor1": True,
        "dirpath": "stockcars2%5Cchevy",
        "abbrevname": "NW09",
        "allowNumberColors": 1,
        "hasRainCapableTireTypes": False,
        "name": "ARCA+Menards+Chevrolet+Impala",
        "uppername": "ARCA+MENARDS+CHEVROLET+IMPALA",
        "pkgid": 71,
        "discountGroupNames": ["oval+car"],
        "allowSelectChrome": True,
        "paintRules": {},
        "maxPowerAdjustPct": "0.0",
        "templatepath": "car_templates%2F24_template_NW09.zip"
    }
    car = map_car(car_dict)
    assert_that(car).is_equal_to(Car(
        id=24,
        name="ARCA Menards Chevrolet Impala"
    ))
