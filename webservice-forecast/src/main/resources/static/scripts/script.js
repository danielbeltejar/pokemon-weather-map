// script.js
/*
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
        
        // Assuming the server responds with an object containing a "base64Image" property
        // representing the base64 encoded image data.
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




const form = document.querySelector('form');
const forecastImage = document.getElementById('forecastImage');

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  fetch('/forecast', {
    method: 'POST',
    body: formData
  })
      .then(response => {
        if (response.ok) {
          return response.blob();
        } else {
          throw new Error('Network response was not ok.');
        }
      })
      .then(imageBlob => {
        const imageUrl = URL.createObjectURL(imageBlob);
        forecastImage.src = imageUrl;
        forecastImage.style.display = 'block'; // Mostrar la imagen una vez que se ha cargado
      })
      .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        // Manejar el error, por ejemplo, mostrar un mensaje de error en el index.html
      });
});



const submitBtn = document.getElementById("submitBtn");
const datePicker = document.getElementById("datePicker");
const resultDiv = document.getElementById("result");
const imageContainer = document.getElementById("imageContainer");
const forecastImage = document.getElementById("forecastImage");

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

          // Assuming the server responds with an object containing a "base64Image" property
          // representing the base64 encoded image data.
          if (forecast.base64Image) {
            const imageUrl = `data:image/png;base64,${forecast.base64Image}`;
            forecastImage.src = imageUrl;
            forecastImage.style.display = 'block'; // Mostrar la imagen una vez que se ha cargado
          } else {
            forecastImage.style.display = 'none';
            resultDiv.textContent += "\nNo image available.";
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
          resultDiv.textContent = "An error occurred while fetching the forecast.";
        });
  } else {
    resultDiv.textContent = "Please select a date.";
  }
});*/
