var sortable = new Sortable(document.getElementById('sortable-list'), {
    animation: 150,  // Smooth animations during drag-and-drop
    ghostClass: 'sortable-ghost',  // CSS class applied during dragging
    handle: '.drag-handle',  // Drag handle selector
});

function deletePhoto(button) {
    const photoId = button.getAttribute('data-photo-id');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const urls = {'delete-photo': '{% url "delete-bike-photo" photo_id=photo_id %}'};

//    fetch(url.delete_photo)
    fetch(`delete-photo/${photoId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
    })
    .then(response => {
        if (response.ok) {
            // If successful, remove the photo item from the DOM
            button.closest('.photo-item').remove();
        } else {
            console.error('Failed to delete photo:', response.status);
        }
    })
    .catch(error => console.error('Error:', error));
}
