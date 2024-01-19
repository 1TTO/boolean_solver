function printTruthTable(truthTable){
    let truthTableBody = document.getElementById("truthTableBody")

    truthTableBody.innerHTML = ""

    for (let i = 0; i < truthTable.length; i++) {
        let currRow = document.createElement("tr")

        if (truthTable[i][truthTable[i].length - 1] === 1) {
            currRow.setAttribute("style", "background-color: #46c742")
        } else if (truthTable[i][truthTable[i].length - 1] === 0) {
            currRow.setAttribute("style", "background-color: #f76359")
        } else {
            currRow.setAttribute("style", "background-color: #b5babd")
        }

        truthTableBody.appendChild(currRow)

        for (let j = 0; j < truthTable[i].length; j++){
            if (i === 0){
                let th = document.createElement("th")
                th.innerText = truthTable[i][j]
                currRow.appendChild(th)
            } else {
                let td = document.createElement("td")
                td.innerText = truthTable[i][j]
                currRow.appendChild(td)
            }
        }
    }
}