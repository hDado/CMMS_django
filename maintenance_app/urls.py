# maintenance_app/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('', views.home, name='home'),
    #dashboard with sidebar (main):
    path('dashboard/', views.dashboard, name='dashboard'),
    #Maintenance : piece detachee : 
    path('stock-piece/', views.Piece, name='piece'),
    #Add equipement :
    path('add-equipements/', views.EquipView, name='add_equip'),
    #add equip category window : 
    path('equips-category/', views.EquipCatView, name='equipcat'),
    #Request (maintenance Intervention)
    path('add-maintenance/', views.MRequestView, name='m_request'),
    
    
    
    path('add_maintenance_app/', views.MaintenanceScheduleView, name='add_maintenance_app'),
    #View maintenance history table :
    path('maintenance-history/', views.PastMaintenanceView, name='maintenance_history_list'),
    #View present and future history tables : 
    path('maintenance-schedule-list/', views.maintenance_schedule_list, name='maintenance_schedule_list'),
    #edit datatable 1 and 2 :
    path('edit/<int:pk>/', views.edit_MaintenanceScheduleView, name='edit_m'),
    #edit past scheduled task (datatable 3)
    path('edit-2/<int:pk>/', views.edit_MaintenanceScheduleView2, name='edit_p'),
    #calendar : all events :
    path('calendar/', views.index, name='index'),
    path('all_events/', views.all_events, name='all_events'), 
    #update task calendar : 
    path('update-task/', views.update_task, name='update_task'),
    #delete event url : 
    path('remove/', views.remove, name='remove'),
    path('kanban/', views.kanban, name='kanban'),
    path('kanban_task/', views.kanban_task, name='kanban_task'),
    path('add_task/', views.add_task, name='add_task'),
    path('update_task_status/<int:task_id>/<str:new_status>/', views.update_task_status, name='update_task_status'),
   

]
