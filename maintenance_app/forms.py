# forms.py
from django import forms
from .models import MaintenanceRequest,CorrectiveMaintenance,PreventiveMaintenance ,EquipmentCategory,Equipment,MaintenanceSchedule, Task, PieceRechange
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field, Row, Column



#=============

class MaintenanceScheduleForm(forms.ModelForm):
    # Explicitly define the scheduled_date field with a widget
    scheduled_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px;'}))
    class Meta:
        model = MaintenanceSchedule
        fields = ['title','machine', 'maintenance_type','description', 'scheduled_date','duration_hours','created_by','assigned_person', 'technique', 'notes']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

#=========================
#Maintenance: Equipement : 
class EquipForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(EquipForm, self).__init__(*args, **kwargs)
        self.fields['effective_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['warranty_expiration'].widget = forms.DateInput(attrs={'type': 'date'})
        #
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
        Row(
            Column('name', css_class='col-md-4'),
            Column('vendor', css_class='col-md-4'),
        ),
        Row(
            Column('vendor_reference', css_class='col-md-4'),
            Column('model', css_class='col-md-4'),
        ),
        Row(
            Column('category', css_class='col-md-4'),
            Column('serial_number', css_class='col-md-4'),
            Column('used_by', css_class='col-md-4'),
        ),
        Row(
            Column('description', css_class='col-md-6'),
        ),
        Row(
            Column('cost', css_class='col-md-4'),
            Column('effective_date', css_class='col-md-4'),
            Column('warranty_expiration', css_class='col-md-4'),
        ),
   
        )

#----- EquipCategory Form :
class EquipCategoryForm(forms.ModelForm):
    class Meta:
        model = EquipmentCategory
        fields = "__all__"
   


#Preventive Maintenance form :
# 
class PreventiveForm(forms.ModelForm):
    class Meta:
        model = PreventiveMaintenance
        fields = "__all__"

class CorrectiveForm(forms.ModelForm):
    class Meta:
        model = CorrectiveMaintenance
        fields = "__all__"

#Request : demande intervention
class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'



#Maintenance : piece de rechange :        
class PieceForm(forms.ModelForm):
    class Meta:
        model = PieceRechange
        fields = "__all__"
        # Example 1: Adding labels
        """
        labels = {
            'emplacement_stockage': 'Code Interne - magazin',
        }
        """
        # Note: This doesn't prevent the field from being submitted, just hides it in the form.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Change CSS class for the 'modele' field
        #self.fields['nom_piece'].widget.attrs['class'] = 'col-md-6'
        #self.fields['modele'].widget.attrs['class'] = 'col-md-6'

        self.fields['date_achat'].widget = forms.DateInput(attrs={'type': 'date'})

        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(

        Div(
            Field('nom_piece', wrapper_class='col-md-6 '),
            Field('modele', wrapper_class='col-md-6 '),
            

            css_class='row',  # Optional, apply a row class to the entire div
        ),
        
        Div(
            Field('code', wrapper_class='col-md-6 '),
            Field('fournisseur', wrapper_class='col-md-6'),
            css_class='row',
        ),
        Div(
            Field('quantite', wrapper_class='col-md-6'),
            Field('prix', wrapper_class='col-md-6'),
            
            css_class='row',
        ),
        Div(
            Field('date_achat', wrapper_class='col-md-6'),
            Field('seuil_minimum', wrapper_class='col-md-6'),
            Field('emplacement_stockage', wrapper_class='col-md-6'),
            Field('garantie_mois', wrapper_class='col-md-6'),
            css_class='row',
        ),
        #    'field1',
        #    'field2',
            # Add more fields as needed
            #forms.Field('modele', css_class='form-control form-inline'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
        
        
        """

        # Modify the widget for the 'date_achat' field
        self.fields['date_achat'].widget = forms.DateInput(attrs={'type': 'date'})
        # Example 3: Adding placeholder
        self.fields['emplacement_stockage'].widget.attrs['placeholder'] = 'Code magazin'
"""