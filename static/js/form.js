$(document).ready(function() {

	$('form').on('submit', function(event) {
		$('#successAlert').text("");
		$('#successAlert').hide();
		$('#errorAlert').hide();
		rangoIP=$('#rangoIPInput').val()
		meth=$('input[name=metodo]:checked', '#formInfoGath').val()
		$('#infoAlert').text("Cargando: " + meth).show();
		if(meth == 'all'){
			metodos = ["enumeracion_rapida","escanear_host_completo","escanear_host_con_parametros","escanear_host_name","escanear_host_os","escanear_host_tcp","escanear_host_udp","escanear_todo"];
			for(m in metodos)
				callPython(rangoIP, metodos[m])
		} else {
			callPython(rangoIP, meth)
		}
		event.preventDefault();

	});

	function callPython(rangoIP, parametros, metodo){
		$.ajax({
			data : {
				ip : rangoIP,
				params : parametros,
				metodo : metodo
			},
			type : 'POST',
			url : 'http://localhost:5000/nmap',
			dataType: 'json'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
				$('#infoAlert').hide();
			} else {
				$('#successAlert').text($('#successAlert').text() + data.domain).show();
				datos = JSON.parse(data.domain.split("\n")[0]);
				
				// Subdominios?
				if(datos["subdomains_"+dominio])
					for(subDom in datos["subdomains_"+dominio])
						if(datos["subdomains_"+dominio][subDom]["domain"] != "")
							callPython(datos["subdomains_"+dominio][subDom]["domain"], metodo)

				$('#errorAlert').hide();
				$('#infoAlert').hide();
			}
		});
	}
});