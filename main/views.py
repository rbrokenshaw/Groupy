from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from main.groupy import return_csv_details, generate_teams

from main.forms import UploadForm, TeamDetailsForm, SaveForm
from main.models import FileUpload, Solutions, SavedSolutions
import pandas as pd
import os
import copy
import time
from django.core.files.base import ContentFile


def home(request):
	form = UploadForm()
	if request.method == 'POST':
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			# create new instance of file upload and save it
			new_upload = FileUpload(
				csv_file = request.FILES['csv_file'])
			new_upload.save()
			
			# save file path in session
			upload_details = {
				'file_path': new_upload.csv_file.path,
			}
			request.session['upload_details'] = upload_details

			return redirect('main-team-details')
	return render(request, 'main/home.html', {
		'form': form
	})

def team_details(request):
	if 'upload_details' in request.session:
		details = request.session['upload_details']
		csv_info = return_csv_details(details['file_path'])
		if csv_info == False:
				messages.warning(request, 'Please upload a valid .csv file.')
				return redirect('main-home')
		form = TeamDetailsForm(csv_info = csv_info)

		# submit team details form
		if request.method == 'POST' and 'team-details' in request.POST:
			form = TeamDetailsForm(request.POST, csv_info = csv_info)
			if form.is_valid():
				team_details = form.cleaned_data
				team_details_list = []
				team_details_list.append(team_details['team_size'])
				team_details_list.append(team_details['iterations'])
				for i in range(10):
					custom_string = "custom_" + str(i)
					for i in team_details:
						if i == custom_string:
							team_details_list.append(team_details[i])
				request.session['team_details_list'] = team_details_list
				return redirect('main-results')

		return render(request, 'main/team-details.html', {
			'csv_info': csv_info,
			'form': form,
		})
	else:
		messages.warning(request, f'Please begin by uploading a file.')
		return redirect('main-home')


def results(request):
	form = SaveForm()
	if 'team_details_list' in request.session:
		
		# save results if user is logged in
		if request.method == 'POST' and 'save' in request.POST:
			if request.user.is_authenticated:
				form = SaveForm(request.POST)
				if form.is_valid():
					if not os.path.exists("media/saved"):
						os.makedirs('media/saved')
					filename = form.cleaned_data['file_name'] + '.csv'

					solution_path = request.session['solution_path']

					df = pd.read_csv(solution_path)

					results_csv = df.to_csv(r'media/saved/' + filename, index = None, header=True)

					save_file = SavedSolutions(
						csv_file = 'saved/' + filename,
						user = request.user,
						name = filename)
					save_file.save()

					messages.success(request, 'Your results have been saved. You can download saved results from your profile page.')

					'''
					# delete everything from session excluding user logged in
					for key in list(request.session.keys()):
						if not key.startswith("_"): # skip keys set by the django system
							del request.session[key]
					'''

					solution_path = request.session['solution_path']
					df = pd.read_csv(solution_path)
					data_html = df.to_html(index=None)
					final_variance_dict = {}
					html_table_list = []

					return render(request, 'main/results.html', {
						'form': form,
						'data_html': data_html,
						'final_variance_dict': final_variance_dict,
						'html_table_list': html_table_list
					})
			else:
				solution_path = request.session['solution_path']
				df = pd.read_csv(solution_path)
				data_html = df.to_html(index=None)
				final_variance_dict = {}
				html_table_list = []

				messages.warning(request, 'You need to be signed in to save results. Please sign in or create an account')
				return render(request, 'main/results.html', {
					'form': form,
					'data_html': data_html,
					'final_variance_dict': final_variance_dict,
					'html_table_list': html_table_list
				})

		# download results as csv
		if request.method == 'POST' and 'download' in request.POST:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename=groupy-results.csv'

			
			solution_path = request.session['solution_path']

			df = pd.read_csv(solution_path)

			df.to_csv(path_or_buf=response,sep=',',float_format='%.2f',index=False,decimal=",")
			return response

		# get team size and weightings from session
		team_details_list = request.session['team_details_list'].copy()

		team_size = team_details_list[0]
		del team_details_list[0]
		iterations = team_details_list[0]
		del team_details_list[0]
		weightings = team_details_list

		# get file path from session
		details = request.session['upload_details']
		file = details['file_path']

		# get the solution
		solution = generate_teams(file, team_size, iterations, weightings)

		if solution == False:
			messages.warning(request, f'Sorry, cannot divide class by requested team size, please adjust team size and try again.')
			return redirect('main-team-details')

		# save generated solutions to database
		solution_csv = solution['df'].to_csv(index=False)

		updated_file = ContentFile(solution_csv)
		timestr = time.strftime("%Y%m%d-%H%M%S")
		updated_file.name = timestr + ".csv"
		
		new_solution = updated_file
		new_solution = Solutions(csv_file = new_solution)
		new_solution.save()

		# save solution id in session
		solution_id = new_solution.pk
		request.session['solution_id'] = solution_id
		solution_path = new_solution.csv_file.path
		request.session['solution_path'] = solution_path

		# display solution
		data_html = solution['df'].to_html(index=False)
		final_variance_dict = solution['final_variance_dict']
		table_list = solution['table_list']

		html_table_list = []

		for i in table_list:
			html_table_list.append(i.to_html())

		# save solution in session
		request.session['final_variance_dict'] = final_variance_dict

		return render(request, 'main/results.html', {
			'form': form,
			'data_html': data_html,
			'final_variance_dict': final_variance_dict,
			'html_table_list': html_table_list
		})
		
	else:
		messages.warning(request, f'Please begin by uploading a file.')
		return redirect('main-home')




	