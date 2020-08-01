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