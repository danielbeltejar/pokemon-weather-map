let country = "spain"

function moveSpan(selectedDiv) {
    const movingSpan = document.getElementById('movingSpan');
    const selectedDivRect = selectedDiv.getBoundingClientRect();
    const containerRect = selectedDiv.closest('.flex').getBoundingClientRect();
    const offsetX = selectedDivRect.left - containerRect.left - 8;
    const offsetY = selectedDivRect.top - containerRect.top;
    country = selectedDiv.id

    movingSpan.style.left = `${offsetX}px`;
    console.log(country)
    const selectedDate = datePicker.value;
    fetchAndDisplayForecast(selectedDate);
}

const divs = document.querySelectorAll('.flex > .map');
divs.forEach(div => {
    div.addEventListener('click', function () {
        moveSpan(this);
    });
});

moveSpan(divs[0])