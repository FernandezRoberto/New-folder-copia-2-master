function changeFormView()
{
  var valor = document.getElementById("prediccionCorrecta");
  var texto = valor.options[valor.selectedIndex].text;
  //debugger;
  if(texto==='No' || texto==='No lo sé')
  {
    $("#medica").hide();
    $("#recetas").hide();
    $("#tratamiento").hide();
    $("#imprimirRecetas").hide();
  }
  else
  {
    $("#medica").show();
    $("#recetas").show();
    $("#tratamiento").show();
    $("#imprimirRecetas").show();
  }
}