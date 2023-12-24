from geopy import Yandex
from config.settings import YANDEX_GEOCODER_API_KEY as API_KEY


class Locator:

    def __init__(self, raw_place: str = None):
        self.place = raw_place

    def location(self, place=None):
        if place is None:
            place = self.place
        return Yandex(api_key=API_KEY).geocode(place)


class FilterFormMixin:
    """Готовит набор параметров фильтрации переданных
    в форме фильтрации для добавления в GET запрос"""

    def get_filled_filter_parameters(self):
        filter_parameters = {}
        get_dict = self.request.GET
        for parameter in get_dict:
            if get_dict[parameter]:
                # if parameter == 'categories':
                #     filter_parameters['categories'] = get_dict.getlist('categories')
                # else:
                filter_parameters[parameter] = get_dict[parameter]
        return filter_parameters

    def filter_parameters(self):
        parameters_for_url = self.request.GET.copy()
        if 'page' in parameters_for_url:
            del parameters_for_url['page']
        filled_parameters = self.get_filled_filter_parameters()
        return parameters_for_url, filled_parameters
