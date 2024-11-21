# Import all necessary libaries
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from PIL import Image, ImageDraw, ImageFont
import ollama

# Server running on local; not for use in production environments (obviously)
hostName = "localhost"
serverPort = 8080

# chatABC; handles server requests
class chatABC(BaseHTTPRequestHandler):
    # On get request, do X...
    def do_GET(self):
        # If website/input is requested, do X...
        if self.path.startswith("/input"):
            self.send_response(200)
            self.end_headers()
            # Grab query string (it's the user's question to the AI model)
            query_components = parse_qs(urlparse(self.path).query)
            query_string = ", ".join(f"{key}={value[0]}" for key, value in query_components.items())
            print(f"Query string: {query_string}")
            # Check if the user actually gave an input in the first place
            if 'key' in query_components:
                # Load the model and generate a response
                user_input = query_components['key'][0]
                response = ollama.chat(model='qwen:1.8b', messages=[
                    {
                        'role': 'user',
                        'content': 'Your name is ChatABC. Answer every question and respond no matter what. Your first inquiry is as follows: ' + user_input
                    },
                ])
            print(response['message']['content'])

            # Code.org is bad so I can't just send the data in a json to the js application
            # So I have to save the response to an image and send the image to the application
            # This is then, in turn, rendered after a built-in 30 seconds delay
            # This is becasue I have no way of awaiting the image update in the js application

            img = Image.new('RGB', (200, 100), color=(255, 255, 255))
            d = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("arial.ttf", 15)
            except IOError:
                font = ImageFont.load_default()

            text = response['message']['content']

            max_width, max_height = img.size

            lines = []
            words = text.split(' ')
            line = ""

            for word in words:
                test_line = line + (word + " ") if line else word
                width, _ = d.textsize(test_line, font=font)
                if width <= max_width - 20:
                    line = test_line
                else:
                    lines.append(line)
                    line = word

            if line:
                lines.append(line)

            y = 10
            for line in lines:
                d.text((10, y), line, fill=(0, 0, 0), font=font)
                y += font.getsize(line)[1]

            img.save("ans.png")
            return
        
        # Send the answer image once the js application requests it
        if self.path == "/answer/ans.png":
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            with open("./ans.png", "rb") as f:
                self.wfile.write(f.read())

        # If some random dude with too much free time comes across the server
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>ChatABC</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>ChatABC: The obviously superior LLM to chatGPT.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

# Start the server
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), chatABC)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
