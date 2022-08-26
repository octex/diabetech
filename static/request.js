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
    var glucose = document.getElementById("glucosa").value;
    var insulin = document.getElementById("insulina").value;
    var date = document.getElementById("fecha").value;
    var notes = document.getElementById("observaciones").value;
    var request = {
        "valor": glucose,
        "insulina": insulin,
        "fecha": date,
        "observaciones": notes
    }
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

function alert_result(code, message)
{
    // result = result.replace("&#34;", '"')
    if(code == '200' || code == '201')
    {
        alert("Succes!")
    }
    else
    {
        alert("An error has been occured:\n" + message)
    }
}