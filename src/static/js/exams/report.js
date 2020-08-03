// Dynamically fill options for selected class
function getSubjects(cls) {
    school = $('#school').val();
    fetch(`${window.location.origin}/exams/subject/class/${cls.value}${ school ? '?school='+school : '' }`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                $('.errorlist li').val(data.error)
            }else {
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
            }             
        })
}

function getSchools() {
    block = $('#block').val();
    district = $('#district').val();
    if (block) {
        url_maker = 'block';
        value = block;
    }else if (district) {
        url_maker = 'district';
        value = district;
    }else {
        return;
    }
    fetch(`${window.location.origin}/exams/schools/${url_maker}/${value}`)
        .then(response => response.json())
        .then(data => {
            let select_element = document.getElementById(`${ block ? 'school' : 'block' }`);
            while (select_element.hasChildNodes()) {  
                select_element.removeChild(select_element.firstChild);
            }
            let opt = document.createElement('option');
            opt.value = '';
            opt.innerHTML = `SELECT ${ block ? 'SCHOOL' : 'BLOCK' }`;
            select_element.appendChild(opt);
            data = data[`${ block ? 'schools' : 'blocks' }`]
            data.forEach((sch) => {
                opt = document.createElement('option');
                opt.value = sch.id;
                opt.innerHTML = sch.school_name || sch.block_name;
                select_element.appendChild(opt);
            })            
        })
}

if($('#class')[0].value && !$('#subject')[0].value) {
    getSubjects($('#class')[0]);
}
if(localStorage.getItem("Success")) {
    $(".msg").append(`<div class="alert alert-success alert-dismissible fade show" role="alert">
    <strong>Saved Successfully!</strong> 
    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
  </div>`); 
  localStorage.removeItem("Success")
}

$('td[contenteditable=true]').on('click', function(){
    document.execCommand('selectAll',false,null);
})

$('#scholastic').click( function() {
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
                localStorage.setItem("Success", "1")
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

$('#co-scholastic').click( function() {
    var table = $('#table').tableToJSON({
        ignoreRows: [0,1],  // To Ignore the first two rows consisting of table heading

        headings: ['first_name',  // Array of Column Header names
        'id',    // Added ID for faster access
        'grade_1',
        'grade_2']
    }); // Convert the table into a javascript object
    // console.log(JSON.stringify(table));
    console.log(table);

    // Clean table values before sending
    table = JSON.stringify(table)
    table = table.replace(/--/g,'')

    // AJAX req to save changes in exam form
    fetch(`${window.location.origin}/exams/exam_form_co_scholastic/save`, {
        method: 'POST',
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            'Content-Type': 'application/json'
        },
        body: table
        })
        .then((res) => res.json())
        .then(function(data) {
            console.log(data)
            if (data['err'] == undefined) {
                localStorage.setItem("Success", "1")
                window.location.reload()
            }else{
                data['err'] = data['err'].replace(/'(.)'/g, '`$1`')
                console.log(data['err'])
                data['err'] = data['err'].replace(/'/g, '"')
                console.log(data['err'])
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

// For HIDING and SHOWING stream option menu
let ele_class = $('#class')[0];

if (ele_class.value != '11' && ele_class.value != '12') {
    document.getElementsByClassName('stream-column')[0].style.display = "none";
    $('form .offset-md-4.col-4:last-child').attr('class', 'col-md-4')
}

$('#class').on('change', function () {
    if(this.value == '11' || this.value=='12') {
        document.getElementsByClassName('stream-column')[0].style.display = "block";
        $('form .col-md-4:last-child').attr('class', 'offset-md-4 col-4')   
    }else{
        document.getElementsByClassName('stream-column')[0].style.display = "none";
        $('form .offset-md-4.col-4:last-child').attr('class', 'col-md-4')
    }
})
