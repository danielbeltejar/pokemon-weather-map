
const zoomedContainer = document.getElementById('zoomed-image-container');
const bodyBackground = document.getElementById("background")

function zoomInImage(selectedDiv) {
    const origImg = selectedDiv.querySelector('img');
    const clonedImg = origImg.cloneNode(true);

    zoomedContainer.appendChild(clonedImg);
    bodyBackground.classList.remove("lg:bg-gray-200")
}

zoomedContainer.addEventListener('click', function () {
    while (zoomedContainer.firstChild) {
        zoomedContainer.removeChild(zoomedContainer.firstChild);
        bodyBackground.classList.add("lg:bg-gray-200")
    }
});