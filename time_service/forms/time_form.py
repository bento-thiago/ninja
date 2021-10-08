from django import forms


class TimeForm(forms.Form):
    time = forms.DateTimeField(
        label='Hora do Servidor', widget=forms.DateInput(format="%d/%m/%Y %H:%M:%S", attrs={'class': 'datepicker'}), input_formats=["%d/%m/%Y %H:%M:%S"])
