$(document).ready(function () {
    $('.select2').select2({
        placeholder: "Seleccionar Instructor",
        allowClear: true
    });

    $('#btn-addAdmin').hover(
        function () {
            $('.mdl-tooltip').css('display', 'block');
        },
        function () {
            $('.mdl-tooltip').css('display', 'none');
        }
    );
});