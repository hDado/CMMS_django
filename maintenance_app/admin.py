# maintenance_app/admin.py
from django.contrib import admin
from .models import Equipment, EquipmentCategory, Technician,PreventiveMaintenance, MaintenanceRequest,CorrectiveMaintenance , MaintenanceSchedule,Person, Events, Task, PieceRechange

#deleted
#admin.site.register(Machine)
#admin.site.register(MaintenanceSchedule)
#admin.site.register(MaintenanceHistory)
#-------
admin.site.register(Person)
admin.site.register(Events)
admin.site.register(Task)
#todo :
admin.site.register(PieceRechange)


#====================
#new logic inspired by odoo : 
admin.site.register(Equipment)
admin.site.register(EquipmentCategory)
admin.site.register(Technician)
admin.site.register(PreventiveMaintenance)
admin.site.register(CorrectiveMaintenance)
#admin.site.register(MaintenanceRequest)