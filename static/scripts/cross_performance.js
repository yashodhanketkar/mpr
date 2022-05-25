$(document).ready(function() {

    var last_valid_selection = null;

    $('#cross_performance_select_data').change(function(event) {

        if ($(this).val().length > 2) {
            $(this).val(last_valid_selection);
        } else {
            last_valid_selection = $(this).val();
        }
        });
});