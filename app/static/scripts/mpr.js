function passwordValidator() {
    var password = document.getElementById("register-password").value;
    var passwordConfirm = document.getElementById("confirm-password").value;
    var registerButton = document.getElementById("register-btn");

    if (password && password == passwordConfirm) {
        registerButton.disabled = false;
    }
    else {
        registerButton.disabled = true;
    }
}

function preferenceShow() {
    document.getElementById("preference").style.cssText = "display: block; visibility: visible";
}

function preferenceReset() {
    const default_attrs = ["acc-3", "f1-3", "pre-3", "rec-3", "roc-3", "normal"];

    for (let x in default_attrs) {
        document.getElementById(default_attrs[x]).checked = true;
    }
}

function dataInputValidator() {
    var last_valid_selection = null;

    if ($(this).value.length > 2) {
        $(this).value(last_valid_selection)
    } else {
        last_valid_selection = $(this).value;
    }
}


$(document).ready(function () {
    
})