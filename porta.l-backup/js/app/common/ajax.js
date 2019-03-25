var app = app || {};
app.cache = app.cache || {};

$( document ).ready(function() {
    _.each($("table.get-ajax"), function(item) {
        app.tableAjaxGet($(item));
    });
});

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

app.escapeHTML =  function(value) {
    return value.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

app.ajaxPost = function($form, successCallback, failureCallback) {
    loader.start();
    var url = $form.attr('url');
    var type = 'POST';
    var data = $form.serializeJSON();
    setTimeout(function(){
        $.ajax({
            url : url,
            type : type,
            contentType: "application/json",
            data : JSON.stringify(data),
            dataType:'json'
        })
        .done(function(response, status, xhr) {
            if(_.isFunction(successCallback)) {
                successCallback(response, status, xhr);
            }
        })
        .fail(function(xhr) {
            if((xhr.status >= 500 && xhr.status < 600) || xhr.statusText == "error") {
                bootbox.alert("Hubo un error procesando su solicitud, contacte al administrador.");
            } else {
                if(xhr.status == 400) {
                    var xhrErrors = xhr.responseJSON.errors;
                    var keys = _.keys(xhrErrors);
                    _.each(keys, function(key) {
                        var errors = xhrErrors[key];
                        validator.addError($form, key, errors);
                    });
                }
                if(_.isFunction(failureCallback)) {
                    failureCallback(xhr, xhr.responseJSON);
                }
            }
        })
        .always(function() {
            loader.stop();
        });
    }, 1500);
}

app.tableAjaxGetRefresh = function($table) {
    $table.find("tbody").empty();
    app.tableAjaxGet($table);
}

app.showTableLoader = function($table) {
    var loaderSelector = $table.attr("loader-selector");
    if(!_.isUndefined(loaderSelector)) {
        tableLoader = $(loaderSelector);
        tableLoader.show();
    } else {
        loader.start();
    }
}

app.hideTableLoader = function($table) {
    var loaderSelector = $table.attr("loader-selector");
    if(!_.isUndefined(loaderSelector)) {
        tableLoader = $(loaderSelector);
        tableLoader.hide();
    } else {
        loader.stop();
    }
}

app.tableAjaxGet = function($table) {
    app.showTableLoader($table);
    var url = $table.attr("url");
    var rowTemplate = _.template(`
      <tr index='<%= index %>'>
      </tr>
    `);
    var columnTemplate = _.template(`
      <td column='<%= column %>' class='<%= columnClass %>'></td>
    `);
    $.ajax({
        url : url,
        type : "GET",
        contentType: "application/json",
        dataType:'json'
    })
    .done(function(response, status, xhr) {
        var key = $table.attr("cache");
        app.cache[key] = response;
        _.each(response, function(data, index) {
            $table.find("tbody").append(rowTemplate({
                index: index
            }));
            $insertedRow = $table.find("tr[index=" + index + "]");
            _.each($table.find("thead th"), function(item, index) {
                var $th = $(item);
                var columnName = _.isUndefined($th.attr("ajax-column")) ? index : $th.attr("ajax-column");
                var columnClass = _.isUndefined($th.attr("column-class")) ? "" : $th.attr("column-class");
                $insertedRow.append(columnTemplate({
                    column : columnName,
                    columnClass: columnClass
                }));
                if($th.hasClass("innerHTML")) {
                    var text = $th.find(".inner-html").html().replace("&lt;","<").replace("&gt;",">");
                    var innerHtml = _.template(text);
                    var templateParameters = $th.attr("template-parameters");
                    var parameters = _.isUndefined(templateParameters) ? [] : templateParameters.split(",");
                    var templateData = {};
                    _.each(parameters, function(parameter) {
                        templateData[parameter] = data[parameter];
                    });
                    $insertedRow.find("td").last().append(innerHtml(templateData));
                }
            });
            _.each(_.keys(data), function(key) {
                var $td = $insertedRow.find("td[column=" + key + "]");
                if($td.length > 0) {
                    $td.html(data[key]);
                }
            });
        });
        app.postTableLoadEvent($table);
    })
    .fail(function(xhr) {
        bootbox.alert("Hubo un error procesando su solicitud, contacte al administrador.");
    })
    .always(function() {
        app.hideTableLoader($table);
    });
}

app.postTableLoadEvent = function($body) {
    var items = $body.find(".replace-confirmation");
    _.each(items, function(item) {
        var $item = $(item);
        if(item.innerHTML === "None") {
            $item.html('<label class="badge badge-success">Confirmado</label>');
        } else {
            $item.html('<label class="badge badge-warning">No Confirmado</label>');
        }
    });
    return $body;
}

app.remove = function(el, url, title, tableSelector) {
    bootbox.confirm({
        title: title,
        message: 'Seleccione una opcion.',
        buttons: {
            cancel: {
                label: '<i class="fa fa-times"></i> Cancelar'
            },
            confirm: {
                label: '<i class="fa fa-check"></i> Continuar'
            }
        },
        callback: function (result) {
            if(!result) return;
            loader.start();
            $.ajax({
                url : url,
                type : "DELETE",
                contentType: "application/json",
                dataType:'json'
            })
            .done(function(response, status, xhr) {
                bootbox.alert(response.message, function(){
                    if(!_.isUndefined(tableSelector)) {
                        app.tableAjaxGetRefresh($(tableSelector));
                    }
                });
            })
            .fail(function(xhr) {
                 if((xhr.status >= 500 && xhr.status < 600) || xhr.statusText == "error") {
                    bootbox.alert("Hubo un error procesando su solicitud, contacte al administrador.");
                } else {
                    if(xhr.status == 400) {
                        var error = _.first(xhr.responseJSON.errors.id).value;
                        bootbox.alert(error);
                    }
                }
            })
            .always(function() {
                loader.stop();
            });
        }
    });
}

app.view = function(el, cacheKey, id, selector) {
    var item = _.find(app.cache[cacheKey], function(item){ return item.id == id; });
    item = _.mapObject(item, function(data) {
        return _.isString(data) && _.isEmpty(data) ? "(No proveido)" : data;
    });
    var innerHtml = _.template($(selector).html().replaceAll("&lt;","<").replaceAll("&gt;",">"));
    var $parsedHtml = $(innerHtml(item));
    $parsedHtml = app.postTableLoadEvent($parsedHtml);
    bootbox.alert({
        message: $parsedHtml.html(),
        callback: function () {
            console.log('This was logged in the callback!');
        }
    }).find("div.modal-content").addClass("largeWidth");
}

