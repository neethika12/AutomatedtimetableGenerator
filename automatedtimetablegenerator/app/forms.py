from django import forms
from .models import TimeTable  # Adjust the import based on your model's location

class TimePickerWidget(forms.TimeInput):
    template_name = 'widgets/time_picker.html'

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = '__all__'
        widgets = {
            'Timestart': TimePickerWidget(),
            'TimeEnd': TimePickerWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get("Day")
        programme = cleaned_data.get("Programme")
        venue = cleaned_data.get("Venue")
        timestart = cleaned_data.get("Timestart")
        timeend = cleaned_data.get("TimeEnd")

        # Check for overlap with the same venue
        overlapping_venue = TimeTable.objects.filter(
            Day=day,
            Venue=venue,
            Timestart__lt=timeend,
            TimeEnd__gt=timestart
        ).exists()

        if overlapping_venue:
            raise forms.ValidationError("This venue is already booked during the selected time.")

        # Optionally, you can check for the lecturer's availability if you have a Lecturer model
        # Here, I'm assuming you have a way to relate the TimeTable with a Lecturer

        return cleaned_data
