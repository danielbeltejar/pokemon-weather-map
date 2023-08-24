
const zoomedContainer = document.getElementById('zoomed-image-container');

function zoomInImage(selectedDiv) {
    const origImg = selectedDiv.querySelector('img');
    const clonedImg = origImg.cloneNode(true);

    zoomedContainer.appendChild(clonedImg);
}

zoomedContainer.addEventListener('click', function () {
    while (zoomedContainer.firstChild) {
        zoomedContainer.removeChild(zoomedContainer.firstChild);
    }
});