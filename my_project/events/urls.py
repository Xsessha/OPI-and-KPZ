from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('create/', views.create_event, name='create_event'),
    path('join/', views.join_event, name='join_event'),

    path('wishlist/<uuid:event_id>/', views.wishlist, name='wishlist'),

    path('draw/<uuid:event_id>/', views.run_draw_view, name='draw'),
    path('assignment/<uuid:event_id>/', views.assignment, name='assignment'),
    path('assignment/<uuid:event_id>/sent/', views.mark_gift_sent, name='mark_gift_sent'),
]