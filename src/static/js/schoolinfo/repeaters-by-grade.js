// Utility function to get csrf-token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('td[contenteditable=true]').on('click', function(){
    document.execCommand('selectAll',false,null);
})

$('#convert-table').click( function() {
    var table = $('#table').tableToJSON({
        ignoreRows: [0,1],  // To Ignore the first two rows consisting of table heading

        headings: [
            'class_name',
            'boys_1','girls_1',  // Array of Column Header names
            'boys_2','girls_2',
            'boys_3','girls_3',
            'boys_4','girls_4',
            'boys_5','girls_5',
            'boys_6','girls_6',
            'boys_7','girls_7',
            'boys_8','girls_8',
            'boys_9','girls_9',
            'boys_10','girls_10',
            'boys_11','girls_11',
            'boys_12','girls_12'        
        ]
    }); // Convert the table into a javascript object
    // console.log(JSON.stringify(table));
    // console.log(table);

    let response = {
        table,
        academic_year: $('#academic_year').children("option:selected").val()
    }
    response = JSON.stringify(response).replace(/-/g, '')

    fetch(`${window.location.origin}/schoolinfo/repeaters-by-grade/save`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json'
        },
        body: response
        })
        .then((res) => res.json())
        .then(function(data) {
            if (data['err'] == undefined) {
                window.location.reload()
            }else{
                data['err'] = data['err'].replace(/'/g, '"')
                data['err'] = JSON.parse(data['err'])
                
                for(let [key, val] of Object.entries(data['err'])) {
                    console.log(val);
                    $(".msg").append(`<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong> ${key} - </strong> ${val}.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>`);
                }
            }
        })
})