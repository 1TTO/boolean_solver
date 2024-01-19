function printKVdiagram(kvDiagram){
    let vars = getKVvars()
    let kvXoffset = vars.vertical.length
    let kvYoffset = vars.horizontal.length
    let verticalKVvarAssignments = getKvBinaryVarAssignments(kvXoffset).reverse()
    let horizontalKVvarAssignments = getKvBinaryVarAssignments(kvYoffset).reverse()
    let kvBody = document.getElementById("kvBody")

    kvBody.innerHTML = ""

    for (let i = 0; i < kvYoffset; i++){
        let currRow = document.createElement("tr")
        kvBody.appendChild(currRow)

        for (let j = 0; j < kvXoffset; j++){
            let td = document.createElement("td") //TODO empty
            td.setAttribute("style", "background-color: #b5babd;");
            td.innerText = ' '
            currRow.appendChild(td)
        }
        if (horizontalKVvarAssignments.length > 0){
            for (let j = 0; j < horizontalKVvarAssignments[i].length; j++) {
                let td = document.createElement("td")

                if (horizontalKVvarAssignments[i].charAt(j) === '1'){ //TODO when 1
                    td.setAttribute("style", "background-color: #ed9f39; border-left: solid black 1px; border-right: solid black 1px;")
                    td.innerText = vars.horizontal[i]
                } else { //TODO when 0
                    td.setAttribute("style", "background-color: #b5babd; border-left: solid black 1px; border-right: solid black 1px;")
                    td.innerText = ' '
                }
                currRow.appendChild(td)
            }
        }
    }

    for (let i = 0; i < kvDiagram.length; i++){
        let currRow = document.createElement("tr")
        kvBody.appendChild(currRow)

        for (let j = 0; j < verticalKVvarAssignments.length; j++){
            let td = document.createElement("td")

            if (verticalKVvarAssignments[j].charAt(i) === '1'){ //TODO when 1
                td.setAttribute("style", "background-color: #43b3f0; border-top: solid black 1px; border-bottom: solid black 1px;")
                td.innerText = vars.vertical[j]
            } else { //TODO when 0
                td.setAttribute("style", "background-color: #b5babd; border-top: solid black 1px; border-bottom: solid black 1px;")
                td.innerText = ' '
            }
            currRow.appendChild(td)
        }
        for (let j = 0; j < kvDiagram[i].length; j++){
            let td = document.createElement("td")

            if (kvDiagram[i][j] === 1){ //TODO when 1
                td.setAttribute("style", "background-color: #46c742; border: solid black 1px;")
                td.innerText = kvDiagram[i][j].toString()
            } else { //TODO when 0
                td.setAttribute("style", "background-color: #f76359; border: solid black 1px;")
                td.innerText = kvDiagram[i][j].toString()
            }
            currRow.appendChild(td)
        }
    }
}

function getKVvars(){
    let verticalVars = document.getElementById("verticalVars").value.replaceAll(" ", "").split(",")
    let horizontalVars = document.getElementById("horizontalVars").value.replaceAll(" ", "").split(",")

    if (verticalVars[0] === "" || horizontalVars[0] === ""){
        let variables = Array.from(new Set(document.getElementById("expression").value.replace(/[^a-zA-Z]/gi, '').split(''))).sort()
        let halfIndex = Math.ceil(variables.length / 2);

        horizontalVars = variables.splice(0, halfIndex)
        verticalVars = variables.splice(-halfIndex)
    }

    return{
        'vertical': verticalVars,
        'horizontal': horizontalVars
    };
}

function getKvBinaryVarAssignments(variablesAmount) {
    let kvVarAssignments = ["01"]

    if (variablesAmount < 1) {
        return []
    }

    for (let i = 1; i < variablesAmount; i++){
        for (let j = 0; j < kvVarAssignments.length; j++){
            kvVarAssignments[j] = kvVarAssignments[j].concat(kvVarAssignments[j].split("").reverse().join(""))
        }

        let newKvVarAssignment = "0".repeat(2 ** i)
        newKvVarAssignment = newKvVarAssignment.concat("1".repeat(2 ** i))

        kvVarAssignments.push(newKvVarAssignment)
    }

    return kvVarAssignments
}