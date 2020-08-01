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
    console.log(table);

    // Clean table values before sending
    table = JSON.stringify(table)
    table = table.replace(/--/g,'')

})