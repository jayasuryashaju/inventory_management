from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('scan/', views.scan_product, name='scan_product'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('check_barcode/', views.check_barcode, name='check_barcode'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),


]