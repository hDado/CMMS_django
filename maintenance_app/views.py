# maintenance_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse 
from .models import PreventiveMaintenance , Technician, CorrectiveMaintenance , MaintenanceRequest,EquipmentCategory, Equipment, MaintenanceSchedule, Events, Task, PieceRechange
from django.utils import timezone
from .forms import PreventiveForm  , TechForm, CorrectiveForm, MaintenanceRequestForm,EquipCategoryForm,MaintenanceScheduleForm, TaskForm, PieceForm, EquipForm
from django.contrib import messages
from crispy_forms.helper import FormHelper
import logging
from django.core.serializers import serialize
#=========================
#Auth : 
def register(request):
    return HttpResponse('This is register page')

def login(request):
    return render(request, 'maintenance_app/login.html')
#


#============

def home(request):
    return render(request, 'maintenance_app/main.html')
#======= sidebar dashboard : 
def dashboard(request):
    return render(request, 'maintenance_app/dashboard.html')

#Maintenance :
#Technician :
def addTechView(request):
    all_tech = Technician.objects.all()
    if request.method == 'POST':
        technician_form = TechForm(request.POST) #call form in forms.py
        if technician_form.is_valid():
            technician = technician_form.save()
            messages.success(request, 'Technicien ajouter a la maintenance')
            return redirect('add_tech')  # Redirect to a list view or another page
         
    else:
        technician_form = TechForm()
    context= {'technician_form' : technician_form}
    return render(request, 'maintenance_app/add_technician.html',context)

#Equipement : 
def EquipView(request):
    equips_all = Equipment.objects.all()
    if request.method == 'POST':
        equip_form = EquipForm(request.POST)
        if equip_form.is_valid():
            equipement = equip_form.save()
            return redirect('add_equip')  # Redirect to a list view or another page
    else:
        equip_form = EquipForm()
    
    return render(request, 'maintenance_app/add_equip.html', {'equip_form': equip_form, 'equips_all' : equips_all})

#equipement Category - Window:
def EquipCatView(request):
    Ecat = EquipmentCategory.objects.all()
    if request.method == 'POST':
        cat_form = EquipCategoryForm(request.POST)
        if cat_form.is_valid():
            category = cat_form.save()
            return redirect("equipcat")  #redirect url
    else:
        cat_form =  EquipCategoryForm()   
    return render(request, 'maintenance_app/equipcat.html', {'cat_form': cat_form})



#
#maintenance request : intervention (add_pm.html)
def add_preventive_maintenance(request): 
    if request.method == 'POST':
        form_p = PreventiveForm(request.POST)
        if form.is_valid():
            form_p.save()
            return redirect('allmp')  # Redirect to a success page
    else:
        form_p = PreventiveForm()

    return render(request, 'maintenance_app/add_pm.html', {'form_p': form_p})
#
#preventive maintenance Calendar :
def allPreventive(request):
    all_events = PreventiveMaintenance.objects.all()
    context = {
        "events" : all_events,
    }   

    return render(request, 'maintenance_app/mpcalendar.html', context)


#done
def all_preventive_maintenance(request):

    all_preventive_maintenance = PreventiveMaintenance.objects.all()
    events = []

    for maintenance in all_preventive_maintenance:
        rrule = {
                'freq': 'daily',
                'interval': maintenance.maintenance_frequency_days,
                'dtstart': maintenance.start_date.isoformat(),
                'until': maintenance.end_date.isoformat() if maintenance.end_date else None
            }
        # Format the start and end dates as ISO strings
        start_date = maintenance.start_date.isoformat()
        end_date = maintenance.end_date.isoformat() if maintenance.end_date else None

        # Construct the event object with title, start, and end
        event = {
            'title': maintenance.activity,
            'start': start_date,
            'end': end_date,
            'rrule': rrule, # Include rrule here
        }

        events.append(event)

    # Return the events as JSON
    return JsonResponse(events, safe=False)

"""
def add_corrective_maintenance(request):
    if request.method == 'POST':
        form_c = CorrectiveForm(request.POST)
        if form_c.is_valid():
            form_c.save()
            return redirect('success_page')  # Redirect to a success page
    else:
        form_c = CorrectiveMaintenanceForm()

    return render(request, 'm_request.html', {'form_c': form_c})
"""
#  
def MRequestView(request):
    request_all = MaintenanceRequest.objects.all()
    if request.method == 'POST':
        m_form = MaintenanceRequestForm(request.POST)
        corrective_m = CorrectiveForm(request.POST)

        if m_form.is_valid() and corrective_m.is_valid():
            maintenance_request = m_form.save(commit=False)
            corrective_maintenance = corrective_m.save()
            maintenance_request.save()  # Save the MaintenanceRequest first to get an id
            maintenance_request.corrective_maintenance_entries.add(corrective_maintenance)
            maintenance_request.save()
            return redirect('m_request')  # Redirect to a list view or another page
    else:
        m_form = MaintenanceRequestForm()
        corrective_m = CorrectiveForm()

    return render(request, 'maintenance_app/m_request.html', {'maintenance_request_form': m_form, 'corrective_maintenance_form': corrective_m})
 



#piece detache : #to be updated - Todo : edit - delete
def Piece(request):
    piece_all= PieceRechange.objects.all()
    if request.method == 'POST':
        piece_form = PieceForm(request.POST)
        if piece_form.is_valid():
            piece_rechange= piece_form.save()
            #messages.success(request, 'Piece de rechange ajouter')  # Add success message
            return redirect('piece')  # Redirect to a list view or another page
    else:
       
        piece_form = PieceForm()
        
    return render(request, 'maintenance_app/piece.html', {'piece_form': piece_form,'piece_all': piece_all })




#Create a View to Show Future and Past Maintenance Schedules
def maintenance_schedule_list(request, status='today'):
    today = timezone.now().date()
    

    future_schedules = MaintenanceSchedule.objects.filter(scheduled_date__gte=today).exclude(scheduled_date=today).order_by('scheduled_date')
    past_schedules = MaintenanceSchedule.objects.filter(scheduled_date__lt=today).order_by('-scheduled_date')
    ongoing_schedules = MaintenanceSchedule.objects.filter(scheduled_date=today).order_by('scheduled_date')
    

    return render(request, 'maintenance_app/maintenance_schedule_list.html', {
        #'schedules': schedules,
        'future_schedules': future_schedules,
        'today_schedules': ongoing_schedules,
        'past_schedules': past_schedules,
        'status': status 
        })
    
    #past schedule:
def PastMaintenanceView(request, status='past'):
    today = timezone.now().date()
    past_schedules = MaintenanceSchedule.objects.filter(scheduled_date__lt=today).order_by('-scheduled_date')

    return render(request, 'maintenance_app/maintenance_history_list.html', {
        #'schedules': schedules,
        'past_schedules': past_schedules,
        'status': status 
        })    



def MaintenanceScheduleView(request):
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST)
        if form.is_valid():
            maintenance_fiche = form.save()
            messages.success(request, 'Maintenance record saved successfully.')  # Add success message
            return redirect('maintenance_schedule_list')  # Redirect to a list view or another page
    else:
        form = MaintenanceScheduleForm()

    return render(request, 'maintenance_app/add_maintenance_app.html', {'form': form})

    


#originale
def edit_MaintenanceScheduleView(request, pk):  

    instance = get_object_or_404(MaintenanceSchedule, pk=pk)
    form = MaintenanceScheduleForm(instance=instance)
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('maintenance_schedule_list')

    return render(request, 'maintenance_app/edit_m.html', {'form': form, 'pk': pk})



def edit_MaintenanceScheduleView2(request, pk):
    instance = get_object_or_404(MaintenanceSchedule, pk=pk)
    form = MaintenanceScheduleForm(instance=instance)
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_history_list')

    
    return render(request, 'maintenance_app/edit_m.html', {'form': form, 'pk': pk})


#Corrective Maintenance calendar : 
#Todo :
def CorrCalView(request):
    all_events = CorrectiveMaintenance.objects.all()
    context = {
        "events" : all_events,
    }   

    return render(request, 'maintenance_app/corrective_calendar.html', context)


#json output data as api :
def all_corr(request):
    all_corr = CorrectiveMaintenance.objects.all()
    out=[]
    for event in all_corr:
        event =({
            'title' : event.name,
            'id' : event.id,
            'start' :event.scheduled_date.isoformat(),
            'end' : event.end_date.isoformat() if event.end_date else None,  # ISO 8601 format or None
        }

        )
        out.append(event)
    return JsonResponse(out, safe=False)
        



#EVENTS CALENDAR : 


def index(request):
    all_events = Events.objects.all()
    context = {
        "events" : all_events,
    }   

    return render(request, 'maintenance_app/index.html', context)


#
def all_events(request):
    all_events = Events.objects.all()
    out=[]
    for event in all_events:
        out.append({
            'title' : event.name,
            'id' : event.id,
            'start' : event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end' : event.end.strftime("%m/%d/%Y, %H:%M:%S"),

        })
    return JsonResponse(out, safe=False)
        



#update calendar tasks : 
#update : 
def update_task(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)



    context = {
        "events" : all_events,
    }   

    return render(request, 'index.html', context)

#Delete events : 

def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

#test kanban : ===============
def kanban(request):
    return render(request, 'maintenance_app/kanban.html')    
   
#=== working example of task : ==========
def kanban_task(request):
    # Get tasks based on the specified status
    tasks = Task.objects.all() #filter(status=status)

    return render(request, 'maintenance_app/kanban_board.html', {'tasks': tasks})

#Kanban update drag and drop : 
def update_task_status(request, task_id, new_status):
    try:
        task = Task.objects.get(id=task_id)
        task.status = new_status
        task.save()
        logging.info(f"Task status updated - Task ID: {task_id}, New Status: {new_status}")
        return JsonResponse({'success': True})
    except Task.DoesNotExist:
        logging.error(f"Task not found - Task ID: {task_id}")
        return JsonResponse({'success': False, 'error': 'Task not found'})
    except Exception as e:
        logging.error(f"Error updating task status - Task ID: {task_id}, Error: {str(e)}")
        return JsonResponse({'success': False, 'error': 'Error updating task status'})

# Post request to add TASK in kanban card : 
#todo : Update kanban card logic - task timing, or merge with intervention
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{form.cleaned_data["title"]}" was created successfully!')
            return redirect('add_task')  # Redirect to the kanban board after adding the task
    else:
        form = TaskForm()

    return render(request, 'maintenance_app/add_task.html', {'form': form}) 




