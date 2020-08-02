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

// Dynamically fill options for selected class
function getSubjects(cls) {
    fetch(`${window.location.origin}/exams/subject/class/${cls.value}`)
        .then(response => response.json())
        .then(data => {
            let select_subject = document.getElementById('subject');
            while (select_subject.hasChildNodes()) {  
                select_subject.removeChild(select_subject.firstChild);
            }
            let opt = document.createElement('option');
            opt.value = '';
            opt.innerHTML = 'SELECT SUBJECT';
            select_subject.appendChild(opt);
            data.subjects.forEach((sub) => {
                opt = document.createElement('option');
                opt.value = sub;
                opt.innerHTML = sub;
                select_subject.appendChild(opt);
            })            
        })
}

$('td[contenteditable=true]').on('click', function(){
    document.execCommand('selectAll',false,null);
})

$('#convert-table').click( function() {
    var table = $('#table').tableToJSON({
        ignoreRows: [0,1],  // To Ignore the first two rows consisting of table heading

        headings: ['first_name',  // Array of Column Header names
        'id',    // Added ID for faster access
        'test_1','notebook_1',
        'sea_1','half_yearly_1',
        'total_1','grade_1',
        'test_2','notebook_2',
        'sea_2','half_yearly_2'
        ,'total_2','grade_2']
    }); // Convert the table into a javascript object
    // console.log(JSON.stringify(table));
    console.log(table);

    // Clean table values before sending
    table = JSON.stringify(table)
    table = table.replace(/--/g,'')

    // AJAX req to save changes in exam form
    fetch(`${window.location.origin}/exams/exam_form/save`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json'
        },
        body: table
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
  });