# maintenance_app/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date



#todo : need update or delete :
class Machine(models.Model):
    name = models.CharField(max_length=100)
    m_model = models.CharField(max_length=100,null=True)
    m_reference = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()


    class Meta:
        app_label = 'maintenance_app'  # Specify the app_label for your application

    
    def __str__(self):
        return self.name

#add person :
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# Todo - 28-02-2024 -- updating Odoo module 
#maintenance Technician :
class Technician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100, default='') #could add supplier list -- !!
    vendor_reference = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, default='Unknown')
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number =  models.CharField(max_length=50, unique=True, default='Unknown')
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effective_date = models.DateField(default=date.today)
    warranty_expiration = models.DateField(default=date(2026,1,1))
    
    Options=[
        ('option1', 'Department'),
        ('option2', 'Employee'),
        ('option3', 'Other'),
    ]
    used_by = models.CharField(max_length=20, choices=Options, default='option1')
    
    def __str__(self):
        return self.name



class PreventiveMaintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    maintenance_frequency_days = models.IntegerField()
    maintenance_duration = models.DurationField()
    expected_mean_time_between_failures = models.DurationField()

    def __str__(self):
        return f"Preventive Maintenance for {self.equipment.name}"
#corrective maintenance :
class CorrectiveMaintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    scheduled_date = models.DateField() #start time
    maintenance_duration = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) #end time
    end_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Calculate end time based on start time and maintenance duration
        if self.scheduled_date and self.maintenance_duration:
            start_time = datetime.combine(self.scheduled_date, datetime.min.time())
            duration_hours = int(self.maintenance_duration)
            duration_minutes = int((self.maintenance_duration - duration_hours) * 60)
            duration = timedelta(hours=duration_hours, minutes=duration_minutes)
            self.end_time = start_time + duration
            self.save(update_fields=['end_time'])
    
    
    
    def __str__(self):
        return f"Corrective Maintenance for {self.equipment.name}"


#todo : modify task kanban : 
class MaintenanceRequest(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('corrective', 'Corrective Maintenance'),
        ('preventive', 'Preventive Maintenance'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    maintenance_type = models.CharField(max_length=10, choices=MAINTENANCE_TYPE_CHOICES)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)
    preventive_maintenance = models.ForeignKey(PreventiveMaintenance, on_delete=models.CASCADE, null=True, blank=True)
    technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.maintenance_type == 'preventive' and self.equipment:
            self.title = f"Preventive Maintenance - {self.equipment.name}"
        super().save(*args, **kwargs)








#===============================================================
class MaintenanceSchedule(models.Model):
 
    TECHNIQUE_CHOICES = [
        ('Technique1', 'Electrique'),
        ('Technique2', 'Mecanique'),
        ('Technique3', 'Pneumatique'),
        ('Technique3', 'Logiciel'),
        ('Technique3', 'Autre'),
        # Add more techniques as needed
    ]
    MType= [
        ('Type1', 'Preventive'),
        ('Type2', 'Corrective'),
        ('Type3', 'Predictive'),
    ]
    title = models.CharField(max_length=200, default='plan de maintenance',)
    maintenance_type = models.CharField(max_length=20, choices=MType, default='Type1')
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    description = models.TextField()
    scheduled_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    assigned_person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True)
    technique = models.CharField(max_length=20, choices=TECHNIQUE_CHOICES, default='Technique1')


    def __str__(self):
        return f"{self.machine.name} - {self.scheduled_date}"

    class Meta:
        app_label = 'maintenance_app'  # Specify the app_label for your application

    def __str__(self):
        return f"{self.machine.name} - {self.scheduled_date}"







#Maintenance ; 
#Piece de rechange :
#----
#pip install Pillow 
#field_name = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,

#Todo:
#  inventory :
class PieceRechange(models.Model):
    nom_piece = models.CharField(max_length=255)
    modele = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True)
    fournisseur = models.CharField(max_length=255, blank=True, null=True)
    quantite = models.PositiveIntegerField(default=0)
    prix = models.DecimalField(max_digits=9, decimal_places=2)
    # Champs supplémentaires liés à la gestion des stocks
    seuil_minimum = models.PositiveIntegerField(blank=True, null=True)
    emplacement_stockage = models.CharField(max_length=100, blank=True, null=True)
    date_achat = models.DateField(blank=True, null=True)
    garantie_mois = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_piece} - {self.code}"


class MaintenanceHistory(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    description = models.TextField()
    completed_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.machine.name} - {self.completed_date}"



class Events(models.Model):
    id= models.AutoField(primary_key=True)
    name= models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank = True)
    end = models.DateTimeField(null=True, blank= True)


    class Meta:
        db_table = "tblevents"



class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ])
    