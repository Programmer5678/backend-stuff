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
text.setAttribute("font-size", "25");
text.setAttribute("fill", "red");
text.setAttribute("text-anchor", "middle");
text.setAttribute("dominant-baseline", "middle");

// Create first <tspan>
const tspan1 = document.createElementNS(svgNS, "tspan");
tspan1.setAttribute("x", "85");
tspan1.setAttribute("dy", "0");
tspan1.textContent = "שדה זה הוא";

// Create second <tspan>
const tspan2 = document.createElementNS(svgNS, "tspan");
tspan2.setAttribute("x", "85");
tspan2.setAttribute("dy", "1.2em");
tspan2.textContent = "שדה חובה";

// Append <tspan> elements to <text>
text.appendChild(tspan1);
text.appendChild(tspan2);

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
newElWrapper.style.backgroundColor = "lightblue"; // Just to see the background
newElWrapper.style.zIndex = "1"

newElWrapper.appendChild(newEl)


//Can just copy this... its just one element
function genPopUp() {

    const newElWrapperCopy = newElWrapper.cloneNode(true)

    // document.getElementById("feedback-form").addEventListener(
    //     "submit", () => {
    //         // newElWrapper.remove()
    //         newElWrapper.style.backgroundColor = "orange"
    //         console.log(newElWrapper, " should be reomved")
    //     }
    // )

    document.addEventListener(
        "submit", (e) => {

            e.stopPropagation(); // Prevent further propagation
            e.preventDefault();

            // newElWrapper.remove()
            newElWrapperCopy.style.backgroundColor = "orange"
            console.log(newElWrapper, " should be reomved")
        }, true
    )

    return newElWrapper


}

//Handle an empty input element. get the input wrapper.
//  add the popup to it. add event listeners to close it
function handleEmptyInput(inputEl) {

    const inputWrapper = document.getElementById(inputEl.name + "-wrapper")
    console.log("inputEl", inputEl, "inputWrapper", inputWrapper)

    if (inputWrapper) {

        const popUpWrapper = genPopUp()

        // popUpWrapper.style.transform = "scale(100)"

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

    }

    else {
        console.log(" does not work...")
    }

}

// document.addEventListener("input", (e) => {
//     console.log("e.target" ,e.target)
//     e.target.addEventListener("input", () => {
//         console.log("same thing from inside")
//     })
// })

// שליחת הטופס במייל
function submitEventHandler(e) {



    alert("here")

    e.preventDefault()

    alert("here")

    const form = document.getElementById('feedback-form');
    // if (!form.checkValidity()) {
    //     form.reportValidity();
    //     return;
    // }


    for (const el of form.elements) {

        console.log("element: ", el.name, el.value)

        if (
            el.value == "" ||
            (el.type == "checkbox"
                && document.querySelectorAll(`input[name=${el.name}]:checked`).length == 0
            )) {

            handleEmptyInput(el)

        }

        else {
            console.log("vallejo", el.type, el.value)
        }
    }

    return


    alert("here again")

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

// document.addEventListener("DOMContentLoaded", () => {

//     const form = document.getElementById("feedback-form");
//     if (form) {
//       form.addEventListener("submit", submitEventHandler);
// } else {
//   console.error("No element with ID 'feedback-form' found.");
// }
//   });



const form = document.getElementById("feedback-form");
form.addEventListener("submit", submitEventHandler)



