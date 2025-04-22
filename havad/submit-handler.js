
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
        script_str += ("document.getElementsByName('" + name + "')[0].value = '" + val + "';\n")
    }

    htmlFile = htmlStart
        + "\n<" + "script>\n"
        + script_str
        + "\ndocument.querySelector('fieldset').disabled = true;\n "
        + "\ndocument.getElementById('send-form').style.display = 'none';\n "
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