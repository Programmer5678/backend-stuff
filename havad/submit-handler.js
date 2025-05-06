


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
        const popUpWrapper = genPopUp("על המפקד הישיר", "להיות איש קשר שונה", "מהמפקד העקיף");
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


    if(
         !handleEmptyInputs() ||
           !validateCommanderPhonesNotSame() ){
        return false
    }

    createReadOnlyFormForDownload() //Create the form for download
}


const form = document.getElementById("feedback-form");
form.addEventListener("submit", submitEventHandler)



