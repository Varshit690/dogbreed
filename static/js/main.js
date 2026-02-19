
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('imageInput');
    const preview = document.getElementById('previewImage');
    const previewWrap = document.querySelector('.preview-wrap');

    if (input) {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Header scroll effect
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.site-header');
        if (window.scrollY > 50) {
            header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
        }
    });
});
