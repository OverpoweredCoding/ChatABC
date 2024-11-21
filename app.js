// WARNING: CHANGES EVERY RUN
// ENSURE THAT URL EXISTS BEFORE DEBUGGING
var coreURL = "87ad-69-167-28-18.ngrok-free.app";

// Preload
function runner() {setScreen("start_screen")}

// Render answer image
function updateAnswer() {
  playSound("https://cdn.pixabay.com/audio/2024/02/07/audio_05ef91af0b.mp3");
  setImageURL("answer", "https://" + coreURL + "/answer/ans.png");
}

// Start
onEvent("start", "click", function( ) {
	console.log("start clicked!");
	setScreen("uix");
});

// Tracker user text input and call API
onEvent("user_input", "input", function( ) {
  onEvent("user_input", "keydown", function(event) {
    if (event.key == "Enter") {
      console.log("user_input text: " + getText("user_input"));
	    setImageURL("data_transmitter", "https://" + coreURL + "/input?key=" + getText("user_input").toString());
	    playSound("https://cdn.pixabay.com/audio/2024/02/07/audio_05ef91af0b.mp3");
	    setTimeout(updateAnswer, 30000);
    }
  });
});

// Main
setTimeout(runner, 1000);
