$(document).ready(function() {
    $(".ajax-form").submit(function(evt) {
        evt.preventDefault();
        var $el = $(evt.target);
        var url = $el.attr("url");
        var method = $el.attr("method");
        var data = $el.serializeJSON();
        $.ajax({
            // la URL para la petición
            url : url,
            // la información a enviar
            // (también es posible utilizar una cadena de datos)
            data : data,
            // especifica si será una petición POST o GET
            type : method,
            // el tipo de información que se espera de respuesta
            dataType : 'json',
            // código a ejecutar si la petición es satisfactoria;
            // la respuesta es pasada como argumento a la función
            success : function(response) {
                bootbox.dialog({
                    title: "",
                    message: response.message,
                    buttons: {
                        sucess:{
                            label: "Aceptar",
                            callback: function() {
                                window.location.href = response.url;
                            }
                        }
                    }       
                });
            },
            // código a ejecutar si la petición falla;
            // son pasados como argumentos a la función
            // el objeto de la petición en crudo y código de estatus de la petición
            error : function(xhr, status) {
                bootbox.dialog({
                    title: "",
                    message: "Error Revise su formulario"       
                });
            }
        });
    });
});