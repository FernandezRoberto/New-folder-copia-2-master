$(document).ready(function() {
    var $userForm = $("#newUserForm");
    validator.init($userForm, function() {
        app.ajaxPost($userForm, function(response) {
            bootbox.alert({
                message: response.message,
                callback: function() {
                    if(!_.isEmpty(response.redirect_url)) {
                        location.href = response.redirect_url;
                    }
                }
            });
        }, function(xhr, response) {
            //Add Validation Error server side
        });
    }, function() {
        bootbox.alert("Debe corregir los errores antes de proceder");
    });
});

