var uploaded_img_url = null;
var canvas = document.getElementById('display-canvas');

// For displaying selected file.
$('.custom-file-input').on('change', function() {
    // Get file name & display.
    var fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(fileName);
    // Create url for this image.
    if (window.URL != undefined) {
        uploaded_img_url = window.URL.createObjectURL(this.files[0]);
    }
});

$('form').submit(function(e) {
    e.preventDefault();
    // Clear previous result.
    $('.text-display-content').html('');
    canvas.width = 0;
    canvas.height = 0;
    // Display.
    $('.loading-spinner').show();
    $('.text-display-container').show();
    // Submit form.
    $.ajax({
        url: '/recognition/recognize/',
        type: 'POST',
        data: new FormData(this),
        success: function (response) {
            // Display response.
            $('.loading-spinner').hide();
            $('.text-display-content').html(JSON.stringify(response, null, 2));

            // Display image.
            var img = new Image;
            img.src = uploaded_img_url;
            img.onload = function() {
                display_img(this, response);
            };
        },
        cache: false,
        contentType: false,
        processData: false
    });
});


function display_img(img, result) {
    var ctx = canvas.getContext('2d');

    canvas.width = img.width
    canvas.height = img.height
    ctx.drawImage(img, 0, 0, img.width, img.height);
    ctx.stroke();

    if (result.success) {
        var sys = result.content.sys;
        var dia = result.content.dia;
        var pul = result.content.pul;
        // Draw sys.
        ctx.beginPath();
        ctx.lineWidth = '5';
        ctx.strokeStyle = 'blue';
        ctx.rect(sys.coordinateX, sys.coordinateY, sys.width, sys.height);
        ctx.stroke();
        // Draw dia.
        ctx.beginPath();
        ctx.strokeStyle = 'yellow';
        ctx.rect(dia.coordinateX, dia.coordinateY, dia.width, dia.height);
        ctx.stroke();
        // Draw pul.
        ctx.beginPath();
        ctx.strokeStyle = 'red';
        ctx.rect(pul.coordinateX, pul.coordinateY, pul.width, pul.height);
        ctx.stroke();
    }
}