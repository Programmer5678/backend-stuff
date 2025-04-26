
// שליחת הטופס במייל
function submitAndEmail(e) {

    alert("siuuu")

    // e.preventDefault()

    const form = document.getElementById('feedback-form');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    const formData = new FormData(form);
    script_str = ""

    for (const [name, val] of formData.entries()) {

        const element = document.querySelector(`[name="${name}"]`);
        if (element.type === 'checkbox') {
            script_str += (`document.getElementById("${name}").querySelector('input[value="${val}"]').checked = true;\n`)
        }
        else{
            script_str += ("document.getElementsByName('" + name + "')[0].value = '" + val + "';\n")
        }
        console.log(name, val)
    }

    htmlFile = htmlStart
        + "\n<" + "script>\n"
        + script_str
        + "\ndocument.querySelector('fieldset').disabled = true;\n "
        + "\ndocument.getElementById('send-form').style.display = 'none';\n "
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
    a.download = 'form_data.html';
    a.click();
    URL.revokeObjectURL(a.href);

}

document.getElementById("send-form").addEventListener("click", submitAndEmail)


// document.getElementById("date-label").addEventListener("click", () => {
//     document.getElementsByName("date")[0].click()
// })

// // document.getElementsByName("date")[0].addEventListener("click", () => {
// //     alert("yoohoo2")
// // })