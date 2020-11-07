from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet)

app_name = 'courses'
urlpatterns = [
     path('subjects/',
         views.SubjectListView.as_view(),
         name='subject_list'),
     path('subjects/<pk>/',
         views.SubjectDetailView.as_view(),
         name='subject_detail'),
     path('courses/<pk>/enroll/',
          views.CourseEnrollView.as_view(),
          name='course_enroll'),
     path('', include(router.urls))

]
