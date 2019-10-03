

from django import forms

class UploadForm(forms.Form):
	csv_file = forms.FileField(label='CSV File')

class TeamDetailsForm(forms.Form):
	team_size = forms.IntegerField(initial=4, min_value=2, max_value=100)
	iterations = forms.IntegerField(initial=1000, min_value=50, max_value=10000)

	def __init__(self, *args, **kwargs):
		csv_info = kwargs.pop('csv_info')
		
		super(TeamDetailsForm, self).__init__(*args, **kwargs)

		for i, attribute in enumerate(csv_info):
			label = attribute + " Weighting"
			self.fields['custom_%s' % i] = forms.IntegerField(label=label, initial=1, min_value=1, max_value=100)

	def extra_answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].label, value)


class SaveForm(forms.Form):
	file_name = forms.CharField(required=True, min_length=2, max_length=40)