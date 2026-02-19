console.log("Dog Breed Identification App Running");
// Image preview for single-page upload
document.addEventListener('DOMContentLoaded', function(){
	const input = document.getElementById('imageInput');
	const preview = document.getElementById('previewImage');
	if(!input) return;
	input.addEventListener('change', function(e){
		const file = e.target.files[0];
		if(!file) { preview.style.display='none'; preview.src=''; return; }
		const url = URL.createObjectURL(file);
		preview.src = url;
		preview.style.display = 'block';
	});
});
