async function syncRequest(method, target, params) {
    const xhttp = new XMLHttpRequest();
    let response = null;

    xhttp.onreadystatechange = await function () {
        if (this.readyState === 4 && this.status === 200) {
            response = xhttp.responseText;
        }
    };

    xhttp.open(method, target, false);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(params);

    return response;
}

function parseBooleanExpression(unparsed){
    let parsed = unparsed.replaceAll(" ", "").replaceAll("\n", "")

    if (parsed.includes(",")){
        let parts = parsed.split("}")
        let parsedParts = []

        parts.forEach(part => {
            part = part.replaceAll(",{", "").replaceAll("{", "")
            parsedParts.push("(" + part.replaceAll(",", "|") + ")")
        })

        parsed = parsedParts.join("&")
    }

    return parsed
}

async function run(){
    let params = {
        expression: parseBooleanExpression(document.getElementById("expression").value),
        onlyTrue: document.getElementById("onlyTrue").checked,
        onlyFalse: document.getElementById("onlyFalse").checked,
        customVarSeq: document.getElementById("customVarSeq").value.replaceAll(" ", "").split(","),
        horizontalVars: document.getElementById("horizontalVars").value.replaceAll(" ", "").split(","),
        verticalVars: document.getElementById("verticalVars").value.replaceAll(" ", "").split(","),
    }
    let response = JSON.parse(await syncRequest("POST", "http://127.0.0.1:5000/", JSON.stringify(params))) //TODO change

    if (response["error"] === ""){
        printTruthTable(response["truthTable"])
        printKVdiagram(response["kvDiagram"])
    }else {
        alert(response["error"])
    }
}