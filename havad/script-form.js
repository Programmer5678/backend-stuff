<script>

  const htmlStart = 
"<!DOCTYPE html>\n" +
"<html lang=\"he\" dir=\"rtl\">\n" +
"\n" +
"<head>\n" +
"    <meta charset=\"UTF-8\">\n" +
"    <title>חוות דעת לקצונה</title>\n" +
"    <style>\n" +
"        body {\n" +
"            font-family: Arial, sans-serif;\n" +
"            direction: rtl;\n" +
"            padding: 20px;\n" +
"        }\n" +
"\n" +
"        label {\n" +
"            display: block;\n" +
"            margin-top: 10px;\n" +
"            font-weight: bold;\n" +
"        }\n" +
"\n" +
"        input,\n" +
"        select,\n" +
"        textarea {\n" +
"            width: 100%;\n" +
"            margin-bottom: 10px;\n" +
"            padding: 5px;\n" +
"        }\n" +
"\n" +
"        table {\n" +
"            width: 100%;\n" +
"            border-collapse: collapse;\n" +
"            margin-bottom: 20px;\n" +
"        }\n" +
"\n" +
"        th,\n" +
"        td {\n" +
"            border: 1px solid #ccc;\n" +
"            padding: 8px;\n" +
"            text-align: right;\n" +
"        }\n" +
"\n" +
"        th {\n" +
"            background-color: #f2f2f2;\n" +
"        }\n" +
"\n" +
"        h2 {\n" +
"            background-color: #e0e0e0;\n" +
"            padding: 10px;\n" +
"        }\n" +
"\n" +
"        button {\n" +
"            padding: 10px 20px;\n" +
"            font-size: 16px;\n" +
"            margin-top: 20px;\n" +
"        }\n" +
"    </style>\n" +
"\n" +
"    <scri" + "pt src=\"https://cdn.jsdelivr.net/npm/pako@2.0.4/dist/pako.min.js\"></scr" + "ipt> <!-- Pako from CDN -->\n" +
"</head>\n" +
"\n" +
"<body>\n" +
"    <h2>חוות דעת המפקד הישיר</h2>\n" +
"    <form id=\"feedback-form\">\n" +
"        <fieldset disabled=\"disabled\">\n" +
"            <label>תאריך:</label>\n" +
"            <input type=\"date\" name=\"date\">\n" +
"\n" +
"            <label>שם פרטי:</label>\n" +
"            <input type=\"text\" name=\"firstName\">\n" +
"\n" +
"            <label>מספר אישי (7 ספרות):</label>\n" +
"            <input type=\"text\" name=\"personalNumber\" pattern=\"\\d{7}\">\n" +
"\n" +
"            <label>החייל משרת תחת פיקודי (בחודשים):</label>\n" +
"            <input type=\"number\" name=\"monthsUnder\" min=\"0\">\n" +
"\n" +
"            <label>מידת היכרות עם החייל:</label>\n" +
"            <select name=\"familiarity\">\n" +
"                <option value=\"\">בחר</option>\n" +
"                <option>טובה מאוד</option>\n" +
"                <option>די טובה</option>\n" +
"                <option>בינונית</option>\n" +
"                <option>קלושה</option>\n" +
"            </select>\n" +
"\n" +
"            <label>תפקיד נוכחי של החייל\\ת:</label>\n" +
"            <input type=\"text\" name=\"role\">\n" +
"\n" +
"            <label>מאפייני החייל - טבלה:</label>\n" +
"            <table>\n" +
"                <thead>\n" +
"                    <tr>\n" +
"                        <th>מאפייני החייל</th>\n" +
"                        <th>הסבר / דוגמה</th>\n" +
"                    </tr>\n" +
"                </thead>\n" +
"                <tbody>\n" +
"                    <tr>\n" +
"                        <td><input type=\"text\" name=\"feature1\" placeholder=\"נקודת חוזק 1\"></td>\n" +
"                        <td><input type=\"text\" name=\"example1\"></td>\n" +
"                    </tr>\n" +
"                    <tr>\n" +
"                        <td><input type=\"text\" name=\"feature2\" placeholder=\"נקודת חוזק 2\"></td>\n" +
"                        <td><input type=\"text\" name=\"example2\"></td>\n" +
"                    </tr>\n" +
"                    <tr>\n" +
"                        <td><input type=\"text\" name=\"feature3\" placeholder=\"נקודת חולשה 1\"></td>\n" +
"                        <td><input type=\"text\" name=\"example3\"></td>\n" +
"                    </tr>\n" +
"                    <tr>\n" +
"                        <td><input type=\"text\" name=\"feature4\" placeholder=\"נקודת חולשה 2\"></td>\n" +
"                        <td><input type=\"text\" name=\"example4\"></td>\n" +
"                    </tr>\n" +
"                </tbody>\n" +
"            </table>\n" +
"\n" +
"            <label>מה מידת המוטיבציה של החייל לצאת לקצונה:</label>\n" +
"            <select name=\"motivation\">\n" +
"                <option value=\"\">בחר</option>\n" +
"                <option>גבוהה מאוד</option>\n" +
"                <option>גבוהה</option>\n" +
"                <option>בינונית</option>\n" +
"                <option>נמוכה</option>\n" +
"                <option>איני רוצה לצאת</option>\n" +
"            </select>\n" +
"\n" +
"            <label>תחומים בהם החייל עלול להתקשות בקורס קצינים / בתפקיד:</label>\n" +
"            <textarea name=\"difficultyAreas\" rows=\"3\"></textarea>\n" +
"\n" +
"            <label>עד כמה מתאים/ה החייל/ת לקצונה ביחס לחיילים אחרים בתפקידים דומים?</label>\n" +
"            <select name=\"suitabilityCompared\">\n" +
"                <option value=\"\">בחר</option>\n" +
"                <option>יותר מרוב החיילים</option>\n" +
"                <option>כמו רוב החיילים</option>\n" +
"                <option>פחות מרוב החיילים</option>\n" +
"                <option>אינו מתאים כלל</option>\n" +
"            </select>\n" +
"\n" +
"            <label>עד כמה תהיה מוכן לקבל את החייל/ת תחת פיקודך כקצין/ה?</label>\n" +
"            <select name=\"willingnessCommand\">\n" +
"                <option value=\"\">בחר</option>\n" +
"                <option>במידה רבה מאוד</option>\n" +
"                <option>במידה רבה</option>\n" +
"                <option>במידה בינונית</option>\n" +
"                <option>במידה מועטה</option>\n" +
"                <option>לא מעוניין כלל</option>\n" +
"            </select>\n" +
"\n" +
"            <h3>פרטי המפקד:</h3>\n" +
"            <label>שם פרטי:</label>\n" +
"            <input type=\"text\" name=\"commanderName\">\n" +
"\n" +
"            <label>טלפון:</label>\n" +
"            <input type=\"text\" name=\"commanderPhone\" pattern=\"\\d{10}\">\n" +
"\n" +
"            <label>משוב לחוות הדעת - שם פרטי:</label>\n" +
"            <input type=\"text\" name=\"feedbackName\">\n" +
"\n" +
"            <label>חתימה:</label>\n" +
"            <canvas id=\"signature-pad\" width=\"400\" height=\"150\" style=\"border:1px solid #ccc;\"></canvas>\n" +
"            <button type=\"button\" onclick=\"clearSignature()\">נקה חתימה</button>\n" +
"\n" +
"            <h2>חוות דעת מפקדו של המפקד הישיר</h2>\n" +
"\n" +
"            <label>משך היכרותך עם החייל (בחודשים):</label>\n" +
"            <input type=\"number\" name=\"monthsUnder2\" min=\"0\">\n" +
"\n" +
"            <label>מידת היכרות:</label>\n" +
"            <select name=\"familiarity2\">\n" +
"                <option value=\"\">בחר</option>\n" +
"                <option>טובה מאוד</option>\n" +
"                <option>די טובה</option>\n" +
"                <option>בינונית</option>\n" +
"                <option>קלושה</option>\n" +
"                <option>איני יכול להעריך</option>\n" +
"            </select>\n" +
"\n" +
"            <label>נקודת חוזק:</label>\n" +
"            <input type=\"text\" name=\"strength2\">\n" +
"\n" +
"            <label>נקודת חולשה:</label>\n" +
"            <input type=\"text\" name=\"weakness2\">\n" +
"\n" +
"            <label>עד כמה תהיה מוכן שהחייל ישרת תחת פיקודך כקצין:</label>\n" +
"            <select name=\"willingnessCommand2\">\n" +
"                <option value=\"\">בחר</option>\n" +
"                <option>במידה רבה מאוד</option>\n" +
"                <option>במידה רבה</option>\n" +
"                <option>במידה בינונית</option>\n" +
"                <option>במידה מועטה</option>\n" +
"                <option>לא מעוניין כלל</option>\n" +
"            </select>\n" +
"\n" +
"            <label>הערות נוספות:</label>\n" +
"            <textarea name=\"additionalComments\" rows=\"3\"></textarea>\n" +
"\n" +
"            <h3>פרטי מפקדו של המפקד הישיר:</h3>\n" +
"            <label>שם פרטי בלבד:</label>\n" +
"            <input type=\"text\" name=\"commander2Name\">\n" +
"\n" +
"            <label>טלפון (10 ספרות):</label>\n" +
"            <input type=\"text\" name=\"commander2Phone\" pattern=\"\\d{10}\">\n" +
"\n" +
"        </fieldset>\n" +
"\n" +
"    </form>\n" +
"\n" +
"    <scr" + "ipt>" + "\n" +
"        // טבלת מאפיינים ודירוגים\n" +
"        // const traits = [\n" +
"        //   \"עצמאות בביצוע משימות\",\n" +
"        //   \"תפקוד יעיל בלחץ ובעומס\",\n" +
"        //   \"קבלת החלטות\",\n" +
"        //   \"משמעת והסתגלות לצרכי המערכת\",\n" +
"        //   \"יכולת חשיבה ולמידה עצמית\",\n" +
"        //   \"עבודת צוות\",\n" +
"        //   \"אומץ איתנות וקור רוח (רק לקרביים)\",\n" +
"        //   \"אסרטיביות ויכולת הובלה\",\n" +
"        //   \"אחריות והשקעה בהתמדה\",\n" +
"        //   \"קבלת ביקורת\"\n" +
"        // ];\n" +
"        // const tableBody = document.getElementById(\"traits-table\");\n" +
"        // traits.forEach((trait, i) => {\n" +
"        //   const row = document.createElement(\"tr\");\n" +
"        //   const tdTrait = document.createElement(\"td\"); tdTrait.textContent = trait; row.appendChild(tdTrait);\n" +
"        //   const tdRating = document.createElement(\"td\");\n" +
"        //   const select = document.createElement(\"select\");\n" +
"        //   select.name = `rating_${i}`; select.required = true;[\"\", \"לא ניתן להעריך\", \"נמוך מאוד\", \"נמוך\", \"בינוני\", \"גבוה\", \"גבוה מאוד\"].forEach(val => {\n" +
"        //     const opt = document.createElement(\"option\"); opt.value = val; opt.textContent = val === \"\" ? \"בחר\" : val; select.appendChild(opt);\n" +
"        //   });\n" +
"        //   tdRating.appendChild(select); row.appendChild(tdRating);\n" +
"        //   tableBody.appendChild(row);\n" +
"        // });\n" +
"\n" +
"        // פונקציה לניקוי חתימה\n" +
"\n" +
"    </scr" + "ipt>\n" +
"\n" +
"    <scr" + "ipt>\n" +
"    \n";


  const htmlEnd = "    </scr" + "ipt>\n" +
"\n" +
"</b" + "ody>\n" +
"\n" +
"</ht" + "ml>\n";

  // console.log("htmlStart start : " , htmlStart , " END")
  // console.log("htmlEnd start : " , htmlEnd , " END")    

      // טבלת מאפיינים ודירוגים
      // const traits = [
      //   "עצמאות בביצוע משימות",
      //   "תפקוד יעיל בלחץ ובעומס",
      //   "קבלת החלטות",
      //   "משמעת והסתגלות לצרכי המערכת",
      //   "יכולת חשיבה ולמידה עצמית",
      //   "עבודת צוות",
      //   "אומץ איתנות וקור רוח (רק לקרביים)",
      //   "אסרטיביות ויכולת הובלה",
      //   "אחריות והשקעה בהתמדה",
      //   "קבלת ביקורת"
      // ];
      // const tableBody = document.getElementById("traits-table");
      // traits.forEach((trait, i) => {
      //   const row = document.createElement("tr");
      //   const tdTrait = document.createElement("td"); tdTrait.textContent = trait; row.appendChild(tdTrait);
      //   const tdRating = document.createElement("td");
      //   const select = document.createElement("select");
      //   select.name = `rating_${i}`; select.required = true;["", "לא ניתן להעריך", "נמוך מאוד", "נמוך", "בינוני", "גבוה", "גבוה מאוד"].forEach(val => {
      //     const opt = document.createElement("option"); opt.value = val; opt.textContent = val === "" ? "בחר" : val; select.appendChild(opt);
      //   });
      //   tdRating.appendChild(select); row.appendChild(tdRating);
      //   tableBody.appendChild(row);
      // }); 

    // פונקציה לניקוי חתימה
    function clearSignature() {
      const canvas = document.getElementById("signature-pad");
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

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
        script_str += ("document.getElementsByName('" + name + "')[0].value = '" + val + "';\n" )
      }

      htmlFile = htmlStart
       + script_str 
       + htmlEnd

      // console.log("htmlFile: " + htmlFile)

      const blob = new Blob([htmlFile], { type: 'text/plain' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'form_data.html';
      a.click();
      URL.revokeObjectURL(a.href);

    }
  </script>