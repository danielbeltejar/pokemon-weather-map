const submitBtn = document.getElementById("submitBtn");
const datePicker = document.getElementById("datePicker");
const resultDiv = document.getElementById("result");
const imageContainer = document.getElementById("imageContainer");

submitBtn.addEventListener("click", () => {
  const selectedDate = datePicker.value;

  if (selectedDate) {
    const url = "https://weather.danielbeltejar.es/v1/forecast";
    const data = {
      date: selectedDate,
    };

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((forecast) => {
        resultDiv.textContent = `Weather forecast for ${selectedDate}: ${JSON.stringify(forecast)}`;

        if (forecast.base64Image) {
          const image = document.createElement("img");
          image.src = `data:image/png;base64,${forecast.base64Image}`;
          imageContainer.innerHTML = "";
          imageContainer.appendChild(image);
        } else {
          imageContainer.innerHTML = "No image available.";
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        resultDiv.textContent = "An error occurred while fetching the forecast.";
      });
  } else {
    resultDiv.textContent = "Please select a date.";
  }
});
