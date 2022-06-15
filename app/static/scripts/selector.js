$(document).ready(function () {
    $("#pref-button").click(
        function(){$("#preference").css({"display": "block", "visibility": "visible"})}
    )
    $('#reset-button').click(
        // function(){$("input:checked").attr('checked', true)}
        function() {
            $('input:radio[name="Accuracy"][value="acc3"]').prop('checked', true),
            $('input:radio[name="F1"][value="f13"]').prop('checked', true),
            $('input:radio[name="Precision"][value="prec3"]').prop('checked', true),
            $('input:radio[name="Recall"][value="rec3"]').prop('checked', true),
            $('input:radio[name="ROC"][value="roc3"]').prop('checked', true),
            $('input:radio[name="Time"][value="normal"]').prop('checked', true)
        }
    )
})