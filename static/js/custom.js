var cols = 6, rows = 4, data = [];
Core = {
    // Make default page
    Init: function(){
        $("#InputValues").removeClass('hidden');
        $("#DataTable").addClass('hidden');
        Core.DrawTable(rows, cols);
    },

    // Check the count of cols, rows
    CheckInputData: function(){
        rows = parseInt($("#RowsNumber").val());
        cols = parseInt($("#ColumnsNumber").val());
        if(!rows || !cols || rows < 4 || cols < 6){
            $(".alert").removeClass('hidden');
            return
        }
        else $(".alert").addClass('hidden');
        Core.rows = rows;
        Core.cols = cols;
        Core.DrawTable(Core.rows, Core.cols);
    },

    // Fill in the table
    DrawTable: function(){
        var data_cols = [];
        for(var i = 0; i < rows; i++){
            for(var j = 0; j < cols; j++){
                data_cols.push(' ');
            }
            data.push(data_cols);
            data_cols = [];
        }
        $("#DataTableDiv").handsontable({
                data: data,
                minSpareRows: 1,
                colHeaders: true,
                rowHeaders: true,
                contextMenu: true
        });
    },

    // Send data to the server
    SendData: function(){
        var header_table = $('table > thead > tr > th > div > span');
        var header = [];
        for(var i = 0; i < cols; i++){
            header.push(header_table[i].textContent);
        }
        $.ajax({
            url: '/',
            type: 'POST',
            dataType: 'JSON',
            data: 'data=' + JSON.stringify(data) + '&head=' + JSON.stringify(header),
            success: function(data){
                alert(data);
            }
        });
    }
};
$(document).ready(Core.Init);