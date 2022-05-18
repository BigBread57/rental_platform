from rest_framework import routers
from rest_framework_nested.routers import NestedSimpleRouter

from api.public.company.views import ReservationViewSet
from api.public.offer.views import OfferViewSet, PriceViewSet, RatingViewSet, BoardOfferViewSet


app_name = 'offer'

router = routers.SimpleRouter()

router.register('', OfferViewSet, basename='offer')


nested_router = NestedSimpleRouter(router, '', lookup='offer')
nested_router.register('rating', RatingViewSet)
nested_router.register('price', PriceViewSet)
nested_router.register('reservation', ReservationViewSet)

router.register('board', BoardOfferViewSet, basename='offer')

urlpatterns = [
    *nested_router.urls,
    *router.urls,
]
