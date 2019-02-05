$(document).ready(function() {

	$("input[type='text']").click(function () {
		$(this).select();
	});

	$('form').on('submit', function(event) { // Esto ordena correctamente las notificaciones y mantiene guardadas todas las "successAlert"
		event.preventDefault();
		try {
			if($('#successAlert1').text() != ''){
				var $divOriginal = $('#successAlert1');
				var $div = $('div[id^="successAlert"]')[1];
				if(typeof($div) == 'undefined'){
					$div = $('#successAlert1');
				}
				try {
					var num = parseInt( $div.prop("id").match(/\d+/g), 10 ) +1;
				} catch(error) {
					var num = parseInt( $div.id.match(/\d+/g), 10 ) +1;
				}

				var $div = $('div[id^="successAlert'+(num-1)+'"]')

				var $klon = $div.clone().prop('id', 'successAlert'+num );
				$divOriginal.after( $klon.text($('#successAlert1').text()) );
			}
			$('#successAlert1').text("");
			$('#successAlert1').hide();
			$('#errorAlert').hide();
			rangoIP=$('#rangoIPInput').val()
			params=$('#parametros').val()
			puerto=$('#puerto').val()
			meth=$('#metodo').children("option:selected").val()
			$('#infoAlert').text("Cargando: " + meth).show();
			if(meth == 'all'){
				metodos = ["enumeracion_rapida","escanear_host_completo","escanear_host_con_parametros","escanear_host_name","escanear_host_os","escanear_host_tcp","escanear_host_udp","escanear_host_tcp_banner_grabbing","escanear_todo"];
				for(m in metodos)
					callPython(rangoIP, params, puerto, metodos[m])
			} else {
				callPython(rangoIP, params, puerto, meth)
			}
		}
		catch(error) {
			console.error(error);
		}
	});

	function callPython(rangoIP, parametros, puerto, metodo){
		var $div = $('div[id^="successAlert"]:last');
		var num = parseInt( $div.prop("id").match(/\d+/g), 10 ) +1;
		$.ajax({
			data : {
				'rangoIP' : rangoIP,
				'params' : parametros,
				'puerto' : puerto,
				'metodo' : metodo
			},
			type : 'POST',
			url : '/nmap',
			dataType: 'json'
		})
		.done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert1').hide();
				$('#infoAlert').hide();
			} else {
				$('#successAlert1').text($('#successAlert1').text() + JSON.stringify(data)).show();
				$('#errorAlert').hide();
				$('#infoAlert').hide();
			}
		});
	}
});