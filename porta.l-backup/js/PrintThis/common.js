function printContent1(id) {
	var restorepage = document.body.innerHTML;
	var printContent = document.getElementById(id).innerHTML;
	document.body.innerHTML = printContent;
	window.print();
	document.body.innerHTML = restorepage;
}

function printContent2(id) {
	var printme = document.getElementById('id');
	var wme = window.open("","","width=900,height=700");
	wme.document.write(printme.innerHTML);
	wme.document.close();
	wme,focus();
	wme.print();
	wme.close();
}

function printData() {
   var divToPrint=document.getElementById("printTable");
   newWin= window.open("");
   newWin.document.write(divToPrint.outerHTML);
   newWin.print();
   newWin.close();
}

function printTableContent(id, title) {
	var $tableContent = $(`
		<br>
		<br>
		<div> Recetas: `+$("#" + id).find("#receta").val()+` </div>
		`);
	$tableContent.find(".noPrint").remove();
	$tableContent.printThis({
	    importCSS: true,
	    loadCSS: "http://localhost:8888/historia_clinica/editar/6192449487634432",
	    importCSS: true,
        importStyle: true,
        margins: "minimum",
	    header: "<h1 class='text-center' style='margin-top:20px;'>" + title + "</h1>"
	});
}

function printContent(id, title) {
	var $Content = $('<br><br>' + $("#" + id)[0].outerHTML);
	$Content.printThis({
	    importCSS: true,
	    loadCSS: "",
	    importCSS: true,
        importStyle: true,
	    header: "<h1 class='text-center' style='margin-top:20px;'>" + title + "</h1>"
	});
}