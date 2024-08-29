from django.urls import path
from .views import AssignMission  ,GetAllMissions ,missions_by_client

urlpatterns = [
    path('add-mission/<int:manager_id>/', AssignMission.as_view(), name='add-assign-mission'),
    path('get-all-missions/', GetAllMissions.as_view(), name='get-all-missions'),
    path('missions-by-client/<int:client_id>/', missions_by_client, name='missions_by_client'),

]
