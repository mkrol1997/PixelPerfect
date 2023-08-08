function modal(){
    $('.modal').modal('show');
}

const image = document.getElementById("new-image");
const form = document.getElementById('image_form');
const src_image = document.querySelector('#id_img_path');

const content = document.getElementById('image-modal')
const loader = document.getElementById('loader')

form.addEventListener('submit', (e) => {
    e.preventDefault();

    content.style.display = 'none';
    loader.style.display = 'block';

    var timestamp = '?t=' + new Date().getTime();
    image.src = ''

    const formData = new FormData(form);
    formData.append('src_image', src_image.files[0]);

    fetch('http://localhost:8000/images/upscale/', {
        method: 'POST',
        body: formData,
    })

    .then(res => res.json())
    .then((json) => {
        loader.style.display = 'none';
        content.style.display = 'block';

        image.src = json.src + timestamp;

        document.getElementById('download').setAttribute("href", 'http://localhost:8000/download/'+json.img_id)
        document.getElementById('saveGDrive').setAttribute("href", 'http://localhost:8000/send-image/'+json.img_id)
    });
});
