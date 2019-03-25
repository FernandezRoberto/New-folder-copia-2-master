"use strict";

/*
    Supported errors:
        required = 1
        onlyLetters = 2
        trainCase = 3
        spaces = 4
        maxLength = 5
        email = 6
        emailInvalid = 7
        minLength = 8
        date = 9
        onlyNumbers = 10
        username = 11
*/
var validator = {
    VALIDATE_CONTAINER: ".validate-container",
    VALIDATE_ERROR_CONTAINER: ".validator-error-container",
    VALIDATE_ERROR: "validate-error",
    updateClass: function($container) {
        var errors = $container.find(this.VALIDATE_ERROR_CONTAINER).find("li");
        if(errors.length > 0) {
            $container.addClass(this.VALIDATE_ERROR);
        } else {
            $container.removeClass(this.VALIDATE_ERROR);
        }
    },
    addError: function($form, key, errors) {
        var $input = $form.find("[name=" + key + "]");
        var $container = $input.closest(validator.VALIDATE_CONTAINER);
        var errorContainer = $container.find(validator.VALIDATE_ERROR_CONTAINER);
        var errorContainerList = errorContainer.find("ul");
        $container.addClass(validator.VALIDATE_ERROR);
        _.each(errors, function(error) {
            if(_.isObject(validator[error.key])) {
                errorContainerList.prepend(validator[error.key].TEMPLATE({
                    value: error.value
                }));
            }
        });
    },
    initValidation: function(type, $input, $container) {
        var self = this;
        $input.change(function(evt) {
            self.validateType.call(self, this, type, evt, $input, $container)
        });
        $input.keyup(function(evt) {
            self.validateType.call(self, this, type, evt, $input, $container)
        });
        $input.keydown(function(evt) {
            self.validateType.call(self, this, type, evt, $input, $container)
        });
        $input.focusout(function(evt) {
            self.validateType.call(self, this, type, evt, $input, $container)
        });
        $input.keypress(function(evt) {
            self.validateType.call(self, this, type, evt, $input, $container)
        });
    },
    validateType: function(el, type, evt, $input, $container) {
        var errorContainer = $container.find(this.VALIDATE_ERROR_CONTAINER);
        var errorContainerList = errorContainer.find("ul");
        var errorLi = errorContainer.find(validator[type].CLASS);
        errorLi.remove();
        if(validator[type].isValid.call(this, $input) === false && ($input.val().length === 0 && $input.attr("validate-required") !== "true") == false) {
            $container.addClass(this.VALIDATE_ERROR);
            var message = $input.attr("validate-" + type + "-message") || validator[type].DEFAULT;
            if(message.indexOf('{length}') >= 0) {
                message = message.replace('{length}', $input.val().length);
            }
            if(message.indexOf('{maxLength}') >= 0) {
                message = message.replace('{maxLength}', $input.attr('validate-maxLength'));
            }
            if(message.indexOf('{minLength}') >= 0) {
                message = message.replace('{minLength}', $input.attr('validate-minLength'));
            }
            if(message.indexOf('{exactLength}') >= 0) {
                message = message.replace('{exactLength}', $input.attr('validate-exactLength'));
            }
            if(_.isObject(validator[type])) {
                errorContainerList.prepend(validator[type].TEMPLATE({
                    value: message
                }));
            }
        }
        this.updateClass.call(this, $container);
    },
    required: {
        CLASS: '.required',
        TEMPLATE: _.template("<li class='required'><%- value %></li>"),
        DEFAULT: 'El campo es requerido.',
        isValid: function($input) {
            var value = $input.val();
            return !_.isEmpty(value);
        }
    },
    onlyLetters: {
        CLASS: '.letters',
        TEMPLATE: _.template("<li class='letters'><%- value %></li>"),
        DEFAULT: 'El campo solo puede contener letras.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            return /^[a-zA-Z áÁéÉíÍóÓúÚüñÑ]+$/.test(value);
        }
    },
    onlyNumbers: {
        CLASS: '.numbers',
        TEMPLATE: _.template("<li class='numbers'><%- value %></li>"),
        DEFAULT: 'El campo solo puede contener números.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            return /^[0-9]+$/.test(value);
        }
    },
    trainCase: {
        CLASS: '.trainCase',
        TEMPLATE: _.template("<li class='trainCase'><%- value %></li>"),
        DEFAULT: 'Cada palabra debe comenzar con mayuscula y las demas letras con minuscula.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var isValid = true;
            var values = _.reject(value.split(' '), function(val){
                return _.isEmpty(val);
            });
            _.each(values , function(item) {
                if(item[0] !== item[0].toUpperCase()) {
                    isValid = false;
                }
                var rest = item.slice(1);
                if(rest !== rest.toLowerCase()) {
                    isValid = false;
                }
            }, this);
            return isValid;
        }
    },
    spaces: {
        CLASS: '.spaces',
        TEMPLATE: _.template("<li class='spaces'><%- value %></li>"),
        DEFAULT: 'No puede usar mas de dos espacios seguidos.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            return /\s\s/.test(value) === false;
        }
    },
    maxLength: {
        CLASS: '.maxLength',
        TEMPLATE: _.template("<li class='maxLength'><%- value %></li>"),
        DEFAULT: 'La maxima longitud es {length}.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var maxLength = parseInt($input.attr("validate-maxlength"));
            return value.length <= maxLength;
        }
    },
    minLength: {
        CLASS: '.minLength',
        TEMPLATE: _.template("<li class='minLength'><%- value %></li>"),
        DEFAULT: 'La minima longitud es {length}.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var minLength = parseInt($input.attr("validate-minLength"));
            return minLength <= value.length;
        }
    },
    exactLength: {
        CLASS: '.exactLength',
        TEMPLATE: _.template("<li class='exactLength'><%- value %></li>"),
        DEFAULT: 'La cantidad requerida de digitos es de {exactLength}, usted tiene {length}.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var exactLength = parseInt($input.attr("validate-exactLength"));
            return exactLength == value.length;
        }
    },
    email: {
        CLASS: '.email',
        TEMPLATE: _.template("<li class='email'><%- value %></li>"),
        DEFAULT: 'El email es invalido.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(String(value).toLowerCase());
        }
    },
    date: {
        CLASS: '.date',
        TEMPLATE: _.template("<li class='date'><%- value %></li>"),
        DEFAULT: 'La fecha es invalida.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var re = /^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$/;
            if(re.test(value) === false) return false;
            var date = moment(value, "DD/MM/YYYY")
            var isValid = true;
            if (moment(date).isValid() === false){
                isValid = false;
            }
            return isValid;
        }
    },
    username: {
        CLASS: '.username',
        TEMPLATE: _.template("<li class='username'><%- value %></li>"),
        DEFAULT: 'El campo debe contener al menos 1 minusculas, 1 mayusculas y un caracter especial entre !@#$&*.',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var re = /^(?=(.*[a-zñ]))(?=(.*[A-ZÑ]))(?=(.*[!@#$&*])).+/;
            return re.test(String(value));
        }
    },
    sameThan: {
        CLASS: '.sameThan',
        TEMPLATE: _.template("<li class='sameThan'><%- value %></li>"),
        DEFAULT: 'Los campos no coinciden',
        isValid: function($input) {
            var value = $input.val();
            if(this.required.isValid.call(this, $input) === false) return true;
            var $anotherInput = $("[" + $input.attr("validate-sameThan") + "]");
            return value == $anotherInput.val();
        }
    }
};

validator.isFormValid = function($form) {
    var self = validator;
    var containers = $form.find(self.VALIDATE_CONTAINER);
    containers.find(self.VALIDATE_ERROR_CONTAINER).find("li").remove();
    _.each(containers, function(container) {
        var $container = $(container);
        var $input = $container.find("input");
        var input = $input[0];
        if($input.length > 0) {
            self.validateType.call(self, this, 'spaces', null, $input, $container);
            if($input.attr("validate-required") === "true") self.validateType.call(self, this, 'required', null, $input, $container);
            if($input.attr("validate-onlyLetters") === "true") self.validateType.call(self, this, 'onlyLetters', null, $input, $container);
            if($input.attr("validate-onlyNumbers") === "true") self.validateType.call(self, this, 'onlyNumbers', null, $input, $container);
            if($input.attr("validate-trainCase") === "true") self.validateType.call(self, this, 'trainCase', null, $input, $container);
            if($input.attr("validate-uppercase") === "true") self.validateType.call(self, this, 'uppercase', null, $input, $container);
            if($input.attr("validate-email") === "true") self.validateType.call(self, this, 'email', null, $input, $container);
            if($input.attr("validate-username") === "true") self.validateType.call(self, this, 'username', null, $input, $container);
            if(!_.isEmpty($input.attr("validate-maxLength"))) self.validateType.call(self, this, 'maxLength', null, $input, $container);
            if(!_.isEmpty($input.attr("validate-minLength"))) self.validateType.call(self, this, 'minLength', null, $input, $container);
            if(!_.isEmpty($input.attr("validate-exactLength"))) self.validateType.call(self, this, 'exactLength', null, $input, $container);
            if(!_.isEmpty($input.attr("validate-sameThan"))) self.validateType.call(self, this, 'sameThan', null, $input, $container);

            if($input.attr("validate-date") === "true") self.validateType.call(self, this, 'date', null, $input, $container);
        }
    }, self);
    return containers.find(self.VALIDATE_ERROR_CONTAINER).find("li").length === 0;
}

validator.init = function($form, callbackSuccess, callbackFailure) {
    var containers = $form.find(this.VALIDATE_CONTAINER);
    _.each(containers, function(container) {
        var $container = $(container);
        var $input = $container.find("input");
        if($input.length > 0) {
            this.initValidation.call(this, 'spaces', $input, $container);
            if($input.attr("validate-required") === "true") this.initValidation.call(this, 'required', $input, $container);
            if($input.attr("validate-onlyLetters") === "true") this.initValidation.call(this, 'onlyLetters', $input, $container);
            if($input.attr("validate-onlyNumbers") === "true") this.initValidation.call(this, 'onlyNumbers', $input, $container);
            if($input.attr("validate-trainCase") === "true") this.initValidation.call(this, 'trainCase', $input, $container);
            if($input.attr("validate-uppercase") === "true") this.initValidation.call(this, 'uppercase', $input, $container);
            if($input.attr("validate-email") === "true") this.initValidation.call(this, 'email', $input, $container);
            if($input.attr("validate-username") === "true") this.initValidation.call(this, 'username', $input, $container);
            if(!_.isEmpty($input.attr("validate-maxLength"))) this.initValidation.call(this, 'maxLength', $input, $container);
            if(!_.isEmpty($input.attr("validate-minLength"))) this.initValidation.call(this, 'minLength', $input, $container);
            if(!_.isEmpty($input.attr("validate-exactLength"))) this.initValidation.call(this, 'exactLength', $input, $container);
            if(!_.isEmpty($input.attr("validate-sameThan"))) this.initValidation.call(this, 'sameThan', $input, $container);

            if($input.attr("validate-date") === "true") this.initValidation.call(this, 'date', $input, $container);
        }
    }, this);
    var self = this;
    $form.submit(function(event) {
        event.preventDefault();
        var func = validator.isFormValid($form) ? callbackSuccess : callbackFailure;
        if(_.isFunction(func)) {
            func();
        }
    });
}

