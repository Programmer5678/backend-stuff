
//Generate a popu element! used for form validation
function genPopUp(...textRows) {
    const svgNS = "http://www.w3.org/2000/svg";

    viewBox = [0, 0, 170, 105]
    // Create SVG element
    const newEl = document.createElementNS(svgNS, "svg");
    newEl.setAttribute("viewBox", viewBox.join(" ")); // 300x180 viewBox
    newEl.setAttribute("xmlns", svgNS);

    newEl.style.width = "100%"
    newEl.style.height = "100%"

    // Create the path element
    const path = document.createElementNS(svgNS, "path");
    path.setAttribute("d", `
            M20,100
            h140
            a10,10 0 0 0 10,-10
            v-50
            a10,10 0 0 0 -10,-10
            h-40
            l20,-20
            -30,20
            h-90
            a10,10 0 0 0 -10,10
            v50
            a10,10 0 0 0 10,10
            z`);

    path.setAttribute("fill", "#ffffff");
    path.setAttribute("stroke", "#000000");
    path.setAttribute("stroke-width", "2");


    // Create the <text> element
    const text = document.createElementNS(svgNS, "text");
    text.setAttribute("x", "85");
    text.setAttribute("y", "52.5");
    text.setAttribute("font-size", "5");
    text.setAttribute("fill", "red");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("dominant-baseline", "middle");


    //dy is the differnece in ys between tspan inside an svg text. increase by 1.2em each row
    let dy = 0
    for (const textRow of textRows) {
        const tspan = document.createElementNS(svgNS, "tspan");
        tspan.setAttribute("x", "85");
        tspan.setAttribute("dy", String(dy) + "em");
        tspan.textContent = textRow; // add text content
        text.appendChild(tspan);

        dy+=1.2
    }


    // Append <tspan> elements to <text>


    // // Set the text content

    // Append path to SVG
    newEl.appendChild(path);

    // Append text to SVG
    newEl.appendChild(text);

    newElWrapper = document.createElement("div")
    newElWrapper.style.position = "absolute";
    newElWrapper.style.top = "0";
    newElWrapper.style.right = "40%"; // Position it at the bottom-right corner
    newElWrapper.style.width = "240px"; // Width of the SVG element
    newElWrapper.style.height = "150px"; // Height of the SVG element
    // newElWrapper.style.backgroundColor = "lightblue"; // Just to see the background
    newElWrapper.style.zIndex = "1"

    newElWrapper.appendChild(newEl)

    // newElWrapperCopy = newElWrapper.cloneNode(true)

    return newElWrapper

}

//Handle an empty input element. get the input wrapper.
//  add the popup to it. add event listeners to close it
//If it is required, return true
function handleEmptyInput(inputEl) {

    const inputWrapper = document.getElementById(inputEl.name + "-wrapper")
    console.log("inputEl", inputEl, "inputWrapper", inputWrapper)

    if (inputWrapper) {

        //Generate popup
        const popUpWrapper = genPopUp("שדה זה הוא", "שדה חובה")

        //append the popup to the input wrapper so it can be placed relative to the inputWrapper(thus the input)
        inputWrapper.appendChild(popUpWrapper)

        const eventListener = () => {
            popUpWrapper.remove() //If exists(safe function), remove
        }


        // All inputs with shared name as our empty input - realistically only that input unless
        // other checkboxes in case we add the event listener to all checkboxes 
        document.querySelectorAll(`input[name="${inputEl.name}"], select[name="${inputEl.name}"], textarea[name="${inputEl.name}"]`)
            .forEach(el => {
                el.addEventListener('input', eventListener);
                el.addEventListener('change', eventListener);
            });

        inputWrapper.addEventListener("click", eventListener)
        //the input wrapper which includes both popup and the input(/s) 
        // itself(themselves in case of checkbox) is here.


        document.getElementById("feedback-form").addEventListener(
            "submit", (e) => {
                popUpWrapper.remove() // Remove popup after submit, new ones will be created
                // e.stopPropagation()
                // e.preventDefault()
            }, true
        )

        return false

    }

    else {
        console.log("input doesnt have wrapper parent - so it is not required!!!")
        return true
    }

}

//Checks if any input that is required(parent has certain parent class - wrapper)
function handleEmptyInputs() {

    const form = document.getElementById('feedback-form');


    for (const el of form.elements) {

        console.log("element: ", el.name, el.value)

        if (
            el.value == "" ||
            (el.type == "checkbox"
                && document.querySelectorAll(`input[name=${el.name}]:checked`).length == 0
            )) {

            if (!handleEmptyInput(el)) {
                return false
            }

        }

    }


    return true

}

function createReadOnlyFormForDownload() {

    const formData = new FormData(form);
    script_str = ""

    for (const [name, val] of formData.entries()) {

        console.log(name, val)


        const element = document.querySelector(`[name="${name}"]`);
        if (element.type === 'checkbox') {
            script_str += (`document.querySelector( 'input[value="${val}"][name="${name}"]' ).checked = true;\n`)
        }
        else {
            script_str += ("document.getElementsByName(" + JSON.stringify(name) + ")[0].value = " +
                JSON.stringify(val) + ";\n")
            console.log("document.getElementsByName('" + JSON.stringify(name) + "')[0].value = '"
                + JSON.stringify(val) + "';\n")
        }
    }

    htmlFile = htmlStart
        + "\n<" + "script>\n"
        + script_str
        + "\ndocument.querySelector('fieldset').disabled = true;\n " //+ No cursor pointer! + No grey input!
        + "\ndocument.querySelectorAll('button').forEach(button => {button.style.display = 'none';});;\n "
        //Click if zoomed in to signature(boo)
        + "\nif (document.getElementById('zoom-out')?.offsetHeight > 0) document.getElementById('zoom-wrapper').click();;\n"


        //Remove cursor pointer:

        + `\ndocument.querySelectorAll('*').forEach(el => {
            const computedStyle = window.getComputedStyle(el);
            if (computedStyle.cursor === 'pointer') {
                el.style.removeProperty('cursor'); // Remove the 'cursor' property if it's set
            }
            });\n`

        + "document.body.classList.toggle('default-backgrounds');"
        + "document.body.offsetHeight;"

        + "\ndocument.querySelectorAll('*').forEach(el => { if (window.getComputedStyle(el).cursor === 'pointer') el.style.cursor = 'default'; });\n"
        + "\nsetCanvasElFromHiddenInput()\n;"
        + "\ncanvas.style.pointerEvents='none' \n"
        + '\nrestoreSelectionsFromInputs()\n'
        + '\ndisableSelecting()\n'
        + "\n<" + "/script>\n"
        + htmlEnd

    // console.log("htmlFile: " + htmlFile)

    const blob = new Blob([htmlFile], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'havad' + formData.get('personalNumber') + '.html';
    a.click();
    URL.revokeObjectURL(a.href);
}

function validateCommanderPhonesNotSame(){

    const formData = new FormData(form);

    if( formData.get('commanderPhone')  == formData.get('commander2Phone')  ) {
        const popUpWrapper = genPopUp("מהמפקד העקיף", "להיות איש קשר שונה", "על המפקד הישיר");
        document.getElementById("commander2Phone-wrapper").appendChild(popUpWrapper)

        const eListener = () => {
            popUpWrapper.remove()
        }

        document.getElementById("commander2Phone-wrapper").addEventListener("click", eListener)
        document.getElementById("commander2Phone").addEventListener("input", eListener)
        document.getElementById("commander2Phone").addEventListener("change", eListener)
        form.addEventListener("submit", eListener)
        
        return false
    }

    return true

}


// שליחת הטופס במייל
function submitEventHandler(e) {

    e.preventDefault() //Ignore submit default


    if( !handleEmptyInputs ||  !validateCommanderPhonesNotSame() ){
        return false
    }

    createReadOnlyFormForDownload() //Create the form for download
}


const form = document.getElementById("feedback-form");
form.addEventListener("submit", submitEventHandler)



