document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has('user_id')) {
        const userId = urlParams.get('user_id');
        const hiddenInput = document.getElementById('user-id-input');
        hiddenInput.value = userId;
        console.log('User ID:', userId);
        console.log('Hidden input value:', hiddenInput.value);
    }
});