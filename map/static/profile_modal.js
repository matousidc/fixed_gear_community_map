function showModal(imageUrl, captionText) {
    var modal = document.getElementById("photoModal");
    var modalImage = document.getElementById("modalImage");
    var modalCaption = document.getElementById("modalCaption");
    modal.style.display = "block";
    modalImage.src = imageUrl;
    modalCaption.textContent = captionText;
}

function hideModal() {
    var modal = document.getElementById("photoModal");
    modal.style.display = "none";
}