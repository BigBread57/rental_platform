from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from api.public.company.views import CompanyViewSet, CompanyRentalPointViewSet, BoardCompanyViewSet, \
    RentalPointViewSet, SlotsAPIView, RentalPointOffersViewSet, RentalPointReservationsViewSet


app_name = 'company'


router = SimpleRouter()
router.register('board', BoardCompanyViewSet)
router.register('rental_points', RentalPointViewSet)
router.register('', CompanyViewSet)

company_rental_points_nested_router = NestedSimpleRouter(router, '', lookup='company')
company_rental_points_nested_router.register('rental_points', CompanyRentalPointViewSet)

rental_point_offers_nested_router = NestedSimpleRouter(router, 'rental_points', lookup='rental_point')
rental_point_offers_nested_router.register('offers', RentalPointOffersViewSet)

rental_point_reservation_nested_router = NestedSimpleRouter(router, 'rental_points', lookup='rental_point')
rental_point_reservation_nested_router.register('reservations', RentalPointReservationsViewSet)

urlpatterns = [
    path('slots/', SlotsAPIView.as_view(), name='slots'),
    *company_rental_points_nested_router.urls,
    *rental_point_offers_nested_router.urls,
    *rental_point_reservation_nested_router.urls,
    * router.urls

]
