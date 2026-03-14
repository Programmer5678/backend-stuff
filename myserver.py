import http.server
import json

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Read content length and data from the request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Optionally parse the data (here, assuming it's JSON)
        try:
            parsed_data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            parsed_data = None

        # Send a response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Respond with the received data (echo it back as JSON)
        response = {
            'status': 'success',
            'received': parsed_data
        }

        # Send the response as JSON
        self.wfile.write(json.dumps(response).encode('utf-8'))

# Set up the server
def run(server_class=http.server.HTTPServer, handler_class=MyHandler):
    server_address = ('', 8080)  # Listen on port 8080
    httpd = server_class(server_address, handler_class)
    print('Starting server on http://localhost:8080')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
