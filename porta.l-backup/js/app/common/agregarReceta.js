function agregarReceta() {
            // get assign the values from each text input
            var receta = document.getElementById('receta');

            // assign multiple text values
            var medicamento = $("#medicamento").val();

            var resultado = receta.value+"º"+medicamento+"\n\n";
            receta.value = resultado;
        }