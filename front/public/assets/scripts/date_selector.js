const submitBtn = document.getElementById("submitBtn");
const datePicker = document.getElementById("datePicker");
const resultDiv = document.getElementById("submitBtn");
const imageContainer = document.getElementById("imageContainer");

submitBtn.addEventListener("click", () => {
  const selectedDate = datePicker.value;

  if (selectedDate) {
    const url = "https://weather.danielbeltejar.es/v1/date/forecast?datePicker=" + selectedDate;

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.blob(); 
        } else {
          throw new Error("Network response was not ok.");
        }
      })
      .then((blob) => {
        const imageUrl = URL.createObjectURL(blob);
        const image = document.getElementById("forecast-image");
        image.src = imageUrl;
        resultDiv.textContent = "Get Forecast";
      })
      .catch((error) => {
        console.error("Error fetching and displaying image:", error);
        resultDiv.textContent = "No forecast yet";
      });
  } else {
    resultDiv.textContent = "Please select a date";
  }
});
