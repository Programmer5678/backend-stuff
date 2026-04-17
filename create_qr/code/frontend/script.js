const API_BASE_URL = "http://127.0.0.1:8000";

async function encode_request(input_path, output_path){

    return await fetch(`${API_BASE_URL}/main/encode`, {
           method: "POST",
           headers: {
               "Content-Type": "application/json"
           },
           body: JSON.stringify({
               input_path: input_path,
               output_path: output_path
           })
       });

}

async function decode_request(input_path, output_path){

    return await fetch(`${API_BASE_URL}/main/decode`, {
           method: "POST",
           headers: {
               "Content-Type": "application/json"
           },
           body: JSON.stringify({
               input_path: input_path,
               output_path: output_path
           })
       });

}

function get_request_func(button_value){
    switch( button_value ){
        case("encode") : return encode_request;
        case("decode") : return decode_request;
        default: alert("submit button value should be encode or decode")
    }

}

function set_result_header(button_value){

    const resultHeader = document.getElementById("result-header");

    switch (button_value) {
        case "encode":
            resultHeader.textContent = "Encode result: \n";
            break;
        case "decode":
            resultHeader.textContent = "Decode result: \n";
            break;
        default:
            alert("Submit button value should be encode or decode");
    }

}

async function set_response(response) {

    document.getElementById("response_code").innerText = response.status
    document.getElementById("response_success").innerText = response.ok ? "SUCCESS" : "FAIL"

    const result_str = JSON.stringify( await response.json() );
    document.getElementById("response_json").innerText = result_str;
}

async function submit_handler(e) {

    e.preventDefault();

    const data = new FormData(e.target);
    set_result_header(e.submitter?.value);

    const request_func = get_request_func(e.submitter?.value);

    const response = await request_func(
        data.get("input_path"),
        data.get("output_path")
    );

    set_response(response);

}

document
    .getElementById("qr-form")
    .addEventListener("submit", submit_handler);















//
//     </form>
//
//+    <div id="result">
//+
//+    <span id="result-header">
//+    </span>
//+
//     <div id="response">
//     <span id="response_json"></span>
//     <span id="response_code"></span>
//     <span id="response_success"></span>
//     </div>
//+    </div>
//
// </body>
//
//diff --git a/code/frontend/script.js b/code/frontend/script.js
//index 83888d9..b29e853 100644
//--- a/code/frontend/script.js
//+++ b/code/frontend/script.js
//@@ -47,10 +47,27 @@ async function set_response(){
//     document.getElementById("response_json").innerText = result_str;
// }
//
//+function set_result_header(){
//+
//+    switch (e.submitter?.value) {
//+        case "encode":
//+            document.getElementById("result-header").textContent = "Encode result: \n";
//+            break;
//+        case "decode":
//+            document.getElementById("response-header").textContent = "Decode result: \n";
//+            break;
//+        default:
//+            alert("Submit button value should be encode or decode");
//+    }
//+
//+}
//+
// async function submit_handler(e) {
//     e.preventDefault();
//
//     const data = new FormData(e.target);
//+
//+    set_result_header(e.submitter?.value);
//     const request_func = get_request_func(e.submitter?.value);
//
//     const response = await request_func(
