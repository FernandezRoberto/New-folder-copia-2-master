function agregarReceta() {
    // get assign the values from each text input
    var receta = document.getElementById('receta');
    // assign multiple text values
    var medicamento = $("#medicamento").val();
    var resultado = receta.value+medicamento+"\n";
    receta.value = resultado;
}

function agregarTratamientos() {
	var valor = document.getElementById("tipoTratamiento");
    var texto = valor.options[valor.selectedIndex].text;
    var resultado = texto;
    receta.value = resultado;
}

function getval(sel)
{
  if(sel.value==='Medicamentos')
  {
    $(".agregarTratamiento").hide();
    $("#medica").show();
    $("#imprimirRecetas").show();
  }
  else
  {
    $(".agregarTratamiento").show();
    $("#medica").hide();
    $("#imprimirRecetas").hide();
  }
}