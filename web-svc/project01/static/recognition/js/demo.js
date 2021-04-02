var uploaded_img_url = null;
var canvas = document.getElementById('display-canvas');


// For displaying selected file.
$('.custom-file-input').on('change', function() {
    // Get file name & display.
    var fileName = $(this).val().split('\\').pop();
    $(this).siblings('.custom-file-label').addClass('selected').html(fileName);

    // Clear text.
    display_text(null);

    if (window.URL != undefined) {
        // Create url for this image.
        uploaded_img_url = window.URL.createObjectURL(this.files[0]);
        // Preview the selected image.
        var img = new Image;
        img.src = uploaded_img_url;
        img.onload = function() {
            display_img(this, null);
        };
    }
});


$('form').submit(function(e) {
    // Change the default form behavior.
    e.preventDefault();
    $form = $(this);

    // Clear previous result.
    $('.text-display-title').html('<h3>解析中 ...</h3>');
    $('.text-display-content').html('');
    canvas.style.display='none';

    // Display.
    $('.loading-spinner').show();
    $('.text-display-container').show();

    // Submit form.
    $.ajax({
        url: $form.attr('action'),
        type: $form.attr('method'),
        data: new FormData(this),
        success: function (response) {
            // Hide spinner.
            $('.loading-spinner').hide();
            // Display text.
            display_text(response);
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


function display_text(response) {
    if (response === null){
        $('.text-display-title').html('');
        $('.text-display-content').html('');
        $('.text-display-container').hide();
    } else if (response.success) {
        var sys = response.result.sys.value;
        var dia = response.result.dia.value;
        var pul = response.result.pul.value;
        $('.text-display-title').html('<h3 style="color:green;">解析成功</h3>');
        $('.text-display-content').html(
            '<h4>收縮壓: ' + sys + '</h4><br>' +
            '<h4>舒張壓: ' + dia + '</h4><br>' +
            '<h4>心率: ' + pul + '</h4>'
        );
    } else {
        $('.text-display-title').html('<h3 style="color:red;">解析失敗</h3>');
        $('.text-display-content').html(
            '<h4>錯誤資訊: ' + response.msg + '</h4>'
        );
    }

}


function display_img(img, response) {
    // Display canvas.
    canvas.style.display='block';

    // Set canvas width.
    canvas.style.width ='100%';
    canvas.width  = canvas.offsetWidth;

    // Calculate ratio.
    ratio = canvas.width / img.width;

    // Set canvas height according to ratio.
    canvas.style.height = Math.ceil(img.height * ratio) + 'px';
    canvas.height = Math.ceil(img.height * ratio);

    // Draw image on canvas.
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvas.width, canvas.height);
    ctx.stroke();

    // Draw rectangles.
    if (response !== null && response.success) {
        // Draw sys.
        var sys = response.result.sys;
        ctx.beginPath();
        ctx.lineWidth = '5';
        ctx.strokeStyle = 'blue';
        ctx.rect(sys.coordinateX*ratio, sys.coordinateY*ratio, sys.width*ratio, sys.height*ratio);
        ctx.stroke();

        // Draw dia.
        var dia = response.result.dia;
        ctx.beginPath();
        ctx.strokeStyle = 'yellow';
        ctx.rect(dia.coordinateX*ratio, dia.coordinateY*ratio, dia.width*ratio, dia.height*ratio);
        ctx.stroke();

        // Draw pul.
        var pul = response.result.pul;
        ctx.beginPath();
        ctx.strokeStyle = 'red';
        ctx.rect(pul.coordinateX*ratio, pul.coordinateY*ratio, pul.width*ratio, pul.height*ratio);
        ctx.stroke();

        // Draw sysTitle.
        if (response.result.hasOwnProperty('sysTitle') && response.result.sysTitle !== null) {
            var sysTitle = response.result.sysTitle;
            ctx.beginPath();
            ctx.lineWidth = '5';
            ctx.strokeStyle = 'blue';
            ctx.rect(sysTitle.coordinateX*ratio, sysTitle.coordinateY*ratio, sysTitle.width*ratio, sysTitle.height*ratio);
            ctx.stroke();
        }

        // Draw diaTitle.
        if (response.result.hasOwnProperty('diaTitle') && response.result.diaTitle !== null) {
            var diaTitle = response.result.diaTitle;
            ctx.beginPath();
            ctx.lineWidth = '5';
            ctx.strokeStyle = 'yellow';
            ctx.rect(diaTitle.coordinateX*ratio, diaTitle.coordinateY*ratio, diaTitle.width*ratio, diaTitle.height*ratio);
            ctx.stroke();
        }

        // Draw pulTitle.
        if (response.result.hasOwnProperty('pulTitle') && response.result.pulTitle !== null) {
            var pulTitle = response.result.pulTitle;
            ctx.beginPath();
            ctx.lineWidth = '5';
            ctx.strokeStyle = 'red';
            ctx.rect(pulTitle.coordinateX*ratio, pulTitle.coordinateY*ratio, pulTitle.width*ratio, pulTitle.height*ratio);
            ctx.stroke();
        }
    }
}