function checkAll() {
    var all = document.getElementById('checkAll');

    if (all.checked == true) {
        var ones = document.getElementsByName('photo');
        for (var i = 0; i < ones.length; i++) {
            ones[i].checked = true;
        }
    } else {
        var ones = document.getElementsByName('photo');
        for (var i = 0; i < ones.length; i++) {
            ones[i].checked = false;
        }
    }
}

function checkOne() {
    var one = document.getElementsByName('photo');
    one.checked = true;
}

function single_delete(image_id) {
    if (confirm('Are you sure you want to delete?')){
        var valArr = [];
        valArr[0] = image_id;
        console.log(valArr)

        if (valArr.length != 0){
            $.ajax({
                url: '/image/delete',
                type: 'POST',
                headers: {
                    'X-HTTP-Method-Override': 'DELETE'
                },
                contenType: 'application/json',
                traditional:true,
                data: {
                    'image_id': valArr
                },
                success: function(){
                    alert('Delete Success');
                    window.location = '/image';
                },
                error: function(){
                    alert('Fail to Delete');
                }
            });
        }
        else {
            var error_m = 'Please choose the photos';
            alert(error_m);
        }
    }
}

function batch_delete() {
    if (confirm('Are you sure you want to delete?')){
        var valArr = [];
        var count = 0;
        var ones = document.getElementsByName('photo');
        
        for (var i = 0; i < ones.length; i++){
            if (ones[i].checked == true){
                valArr[count] = ones[i].value;
                count++;
            }
        }
        
        if (valArr.length != 0){
            $.ajax({
                url: '/image/delete',
                type: 'POST',
                headers: {
                    'X-HTTP-Method-Override': 'DELETE'
                },
                contenType: 'application/json',
                traditional:true,
                data: {
                    'image_id': valArr
                },
                success: function(){
                    alert('Delete Success');
                    window.location = '/image';
                },
                error: function(){
                    alert('Fail to Delete');
                }
            });
        }
        else {
            var error_m = 'Please choose the photos';
            alert(error_m);
        }
    }
}

function single_download(image_id) {
    var valArr = [];
    valArr[0] = image_id;
    
    if (valArr.length != 0){
        $.ajax({
            url: '/image/download',
            type: 'GET',
            contenType: 'application/json',
            traditional:true,
            data: {
                'image_id': valArr
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function(response, status, xhr){
                // get file name in response
                var filename = "";
                var disposition = xhr.getResponseHeader('Content-Disposition');

                if (disposition && disposition.indexOf('attachment') !== -1) {
                    var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    var matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) { 
                      filename = matches[1].replace(/['"]/g, '');
                    }
                }

                var a = document.createElement('a');
                var url = window.URL.createObjectURL(response);

                a.href = url;
                a.download = filename;
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                // window.location = '/image';
            },
            error: function(){
                alert('Fail to Download');
            }
        });
    }
    else {
        var error_m = 'Please choose the photos';
        alert(error_m);
    }
}

function batch_download() {
    var valArr = [];
    var count = 0;
    var ones = document.getElementsByName('photo');
    
    for (var i = 0; i < ones.length; i++){
        if (ones[i].checked == true){
            valArr[count] = ones[i].value;
            count++;
        }
    }
    if (valArr.length != 0){
        $.ajax({
            url: '/image/download',
            type: 'GET',
            traditional:true,
            data: {
                'image_id': valArr
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function(response, status, xhr){
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(response);

                a.href = url;
                a.download = 'images.zip';
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                window.location = '/image';
            },
            error: function(){
                alert('Fail to Download');
            }
        });
    }
    else {
        var error_m = 'Please choose the photos';
        alert(error_m);
    }
}