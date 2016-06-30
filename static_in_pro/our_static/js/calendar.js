 $(function(){
    $('#datepicker').datepicker().on('changeDate', 
    	function(ev){    
			$('#datepicker').datepicker('hide');
			});
	});