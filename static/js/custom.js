var cols = 6, rows = 4, data = [];
Core = {
    // Make default page
    Init: function(){
        $("#InputValues").removeClass('hidden');
        $("#DataTable").addClass('hidden');
        Core.MakeData(rows, cols);
        Core.DrawTable(data);
    },

    // Check the count of cols, rows
    CheckInputData: function(){
        rows = parseInt($("#RowsNumber").val());
        cols = parseInt($("#ColumnsNumber").val());
        if(!rows || !cols || rows < 4 || cols < 6){
            $("#WrongNumber").removeClass('hidden');
            return
        }
        else $("#WrongNumber").addClass('hidden');
        data = [];
        Core.DrawTable(rows, cols);
    },

    // Fill in the table data
    MakeData: function(rows, cols){
        var data_cols = [];
        for(var i = 0; i < rows; i++){
            for(var j = 0; j < cols; j++){
                data_cols.push(' ');
            }
            data.push(data_cols);
            data_cols = [];
        }
    },
    DrawTable: function(data){
        $("#DataTableDiv").handsontable({
                data: data,
                minSpareRows: 1,
                colHeaders: true,
                rowHeaders: true,
                minRows: 4,
                minCols: 6,
                maxRows: rows,
                maxCols: cols,
                contextMenu: true
        });
    },

    // Send data to the server
    SendData: function(){
        $("#InvalidValues").addClass('hidden');
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
            success: function(result){
                if(result.error){
                    $("#InvalidValues").html(result.error).removeClass('hidden');
                    return;
                }
                for(var i = 0; i < data.length; i++){
                    data[i][data[i].length] = result.result[i];
                }
                Core.DrawTable(data);
            }
        });
    }
};
$(document).ready(Core.Init);