const submitBtn = document.getElementById("submitBtn");
const datePicker = document.getElementById("datePicker");
const resultDiv = document.getElementById("submitBtn");
const imageContainer = document.getElementById("imageContainer");

// Set the date picker to today's date
const today = new Date().toISOString().split('T')[0];
datePicker.value = today;

submitBtn.addEventListener("click", () => {
    const selectedDate = datePicker.value;
    fetchAndDisplayForecast(selectedDate);
});

function fetchAndDisplayForecast(date) {
    if (date) {
        const url = "https://weather.danielbeltejar.es/api/forecast?date=" + date.replaceAll("-", "/") + "&country=" + country;

        fetch(url, {
            method: "GET",
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
}

// Fetch and display forecast when the page loads
window.onload = () => {
    fetchAndDisplayForecast(today);
};
