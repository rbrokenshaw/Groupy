<h1>Requirements:</h1>

<ul>
	<li>Python 3.7.4</li>
	<li>Django 2.2.3</li>
	<li>Pandas 0.25.0</li>
	<li>django-crispy-forms-1.7.2</li>
</ul>

<h1>Current CSV Rules</h1>

<ul>
	<li>For gender constraint, gender column must have header 'Gender' (not case sensitive) and genders must be represented by either 'f' or 'm' (not case sensitive)</li>
	<li>For ethnicity constraint, ethnicity column must have header 'Ethnicity' (not case sensitive) and ethnicity must be represented by (not case sensitive):
		<ul>
			<li>'H' - Home student</li>
			<li>'EU' - EU student</li>
			<li>'O' - Overseas student</li>
		</ul>
	</li>
	<li>For academic score constraint, column must have header 'Score' (not case sensitive), and score must be between 0-100.</li>
</ul>