from django.urls import path
from . import views
urlpatterns = [
    path('doctor',views.doc_sign,name='doctor'),
    path('patient',views.pat_sign,name='patient'),
    path('doc_login',views.doc_login,name='doc_login'),
    path('pat_login',views.pat_login,name='pat_login'),
]
