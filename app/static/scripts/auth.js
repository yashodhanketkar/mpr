$(document).ready(function () {
    $(':input[type="submit"]').prop('disabled', true)
    $('#pass, #cpass').on('keyup', function () {
        if ($('#pass').val() == $('#cpass').val()) {
            $(':input[type="submit"]').prop('disabled', false)
        } else {
            $(':input[type="submit"]').prop('disabled', true)
        }
    });
})