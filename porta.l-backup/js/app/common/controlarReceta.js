function changeFormView()
{
  var valor = document.getElementById("prediccionCorrecta");
  var texto = valor.options[valor.selectedIndex].text;
  //debugger;
  if(texto==='No' || texto==='No lo sé')
  {
    $("#medica").hide();
    $("#recetas").hide();
    $("#imprimirRecetas").hide();
  }
  else
  {
    $("#medica").show();
    $("#recetas").show();
    $("#imprimirRecetas").show();
  }
}