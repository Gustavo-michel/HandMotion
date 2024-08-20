chrome.action.onClicked.addListener((tab) => {
    fetch("http://localhost:5000/start-tracking")
      .then(response => response.json())
      .then(data => {
        console.log("Tracking started:", data);
      })
      .catch(error => {
        console.error("Error starting tracking:", error);
      });
  });