function basic_request_parse(method, path, data)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open(method, path, false); // false for synchronous request
    xmlHttp.setRequestHeader('Content-type','application/json; charset=utf-8');
    if (data == null)
    {
        xmlHttp.send(null);
    }
    else
    {
        xmlHttp.send(data);
    }
    return xmlHttp.responseText;
}

function create_registry(path)
{
    var glucose = document.getElementById("glucoseForm").value;
    var insulin = document.getElementById("insulinForm").value;
    var date = document.getElementById("dateForm").value;
    var notes = document.getElementById("notesForm").value;
    var moment = document.getElementById("momentForm").value;
    var food = document.getElementById("foodForm").value;
    var request = {"glucose": glucose, "insulin": insulin, "date": date, "notes": notes, "moment": moment, "food": food}
    var json = JSON.stringify(request)
    var response = basic_request_parse('POST', path, json);
    document.write(response);
    return response
}

function delete_registry(path)
{
    return basic_request_parse('DELETE', path, null);
}

function update_registry(path, data)
{
    return basic_request_parse('PUT', path, data);
}