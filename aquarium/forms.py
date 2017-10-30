from django import forms

class DegreeChartForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput( attrs={ 'type' : 'date' } )
                                    )

    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'})
                                 )

