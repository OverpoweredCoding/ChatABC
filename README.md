# Welcome to ChatABC!

Hello! I'm just an innocent LLM called ChatABC. There's nothing to see here! Keep scrolling...


# Installation Instructions

 1. Run ````python -m pip install ollama````
 2. Run ``python -m pip install pillow``
 3. Install the ollama CLI [here](https://ollama.com/download/OllamaSetup.exe)
 4. Run ````ollama run qwen:1.8b```` (After it finishes verifying SHA256, you can close the window)
 5. Install ngrok [here](https://ngrok.com/)
 6. Run ````ngrok.exe http 8080````
 7. Copy paste the URL into the core URL variable of the javascript application
 8. Run the javascript application

# How do I use it?

Follow the steps above to start to local server. This will become the sorce by which the application draws it's answers when the user inputs questions. After the local server is running, click start on the web application. Upon waiting a few seconds, the loading screen should fade away and the user will be presented with a start button. Pressing this launches a chat window. Simply type your chats into the text box and press enter and an API call will be sent to the local server. After approximately 30 seconds, the server will return a reply and the web application will render it in the black space above the text box. Do not press enter multiple times - this will only make the process take longer.

# Live Application

A link to the web application can be found [here](https://studio.code.org/projects/applab/YvT1JCEPzOhe3nEVK9zztcyW5_n71eTiMDkcvpm4qI8)

# "Devlog"

I wanted to create something interesting for this project and thought that a chatbot sounded cool. Initially I believed that this entire project was going to be in python, so I was surprised to learn that the app was being manipulated purely by python. Despite this, I figured I  should still be able to create the chatbot. My original idea was that the user would input some text and that text would then be sent to a local server using a POST request in JSON format, looking something like this: {"text":"blah blah blah"}. After this request was received the local server would then process the data, formulate a reply, can send it back to the code.org web server with another POST request in JSON format. This would have worked amazingly in theory. But in reality, there was a slight problem: code.org does not support web requests and has nearly all web activity limited to a select few hostnames. This meant that my original idea would not be possible; however, I did not give up on the general concept. It turn out that while code.org limits the hostnames available to vanilla requests, it does not limit the hostnames used when specifying an image's source. Okay... that's great but how does this help with transmitting data? Well, I'm glad you asked - it turns out that code.org also doesn't care if there simply isn't an image at your specified URL and will not throw an error for this case. Additionally, they do not check if you are using a query string. This means that I could update an image with dimensions of 0px by 0px to my local server's URL and pass the user's input through this request by use of query strings. And that is exactly what I did. The only issue with this bandaid solution is the fact that it only allows for 1 way communication - there isn't a way for me to send text back to the web application. Unless... That's right - I used the same exact trick as I did above. When I want to display the output of the local server, I write ans.png to the project's directory. This png contains the text response of the AI. When I want the web server to view this response, I update an empty image to my local server at the endpoint /answer/ans.png and the text magically appears on the screen in front of the user. After getting this working, it was just a matter of polishing up a couple of methods and the app was complete.
