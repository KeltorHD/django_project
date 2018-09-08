$('select').multipleSelect();

$('#id_date').datepicker({
	todayButton:new Date(),
	dateFormat: 'yyyy-mm-dd',
	altField:'yyyy-mm-dd',
	autoClose: true,
	clearButton: true,
	keyboardNav: false
})