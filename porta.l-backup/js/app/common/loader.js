var loader = loader || {};

loader.start = function() {
    $("body").css("pointer-events", "none");
    $("#loader").show();
}

loader.stop = function() {
    $("body").css("pointer-events", "");
    $("#loader").hide();
}
