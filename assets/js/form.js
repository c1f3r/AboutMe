var disable_form = function () {
    $('input').attr('disabled', true);
    $('textarea').attr('disabled', true);
    $('#ajax_progress').show();
    $('#ajax_success').hide();
    $('.alert-danger').remove();
    $('.col-xs-9').removeClass('has-error');
};

var enable_form = function () {
    $('input').removeAttr('disabled');
    $('textarea').removeAttr('disabled');
    $('#ajax_progress').hide();
    $('#ajax_success').show().delay(2000).fadeOut();

};

var form_error = function (response) {
    enable_form();
    $('#ajax_success').hide();
    var errors = JSON.parse(response.responseText);
    console.log(errors);
    for (error in errors) {
        var id = '#id_' + error;
        $(id).parent('div').addClass('has-error');
        if ($(id).parent('div').find('div.alert').length == 0) {
            $(id).parent('div').prepend('<div class="alert alert-danger" id=' + error + '"_error_alert">' + errors[error] + '</div>');
        }

    }

};

$(function () {
    $("#id_avatar").on("change", function () {
        var id = '#id_avatar';
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            console.log($(id).parent);
            $('.btn-success').removeAttr('disabled');
            $(id).parent('div').removeClass('has-error');
            $(id).parent('div').find('div.alert').remove();
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                $("#imagePreview").css("background-image", "url(" + this.result + ")");
            }
        }
        else {
            $('.btn-success').attr('disabled', true);
            $(id).parent('div').addClass('has-error');
            if ($(id).parent('div').find('div.alert').length == 0) {
                $(id).parent('div').prepend('<div class="alert alert-danger" id="avatar_error_alert">Not image!</div>');
            }
        }
    });
});


$(document).ready(function () {
    var options = {
        beforeSubmit: disable_form,
        success: enable_form,
        error: form_error
    };

    $('#edit_info_form').ajaxForm(options);
});
