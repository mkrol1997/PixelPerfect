const image = document.getElementById("new-image");
const form = document.getElementById('image_form');
const src_image = document.querySelector('#id_img_path');

function show_modal(){
    $('.modal').modal('show');
}

function toggle_loader(){
    const content = document.getElementById('image-modal')
    const loader = document.getElementById('loader')

    if (content.style.display == 'none') {
        loader.style.display = 'none';
        content.style.display = 'block';
    }
    else {
        content.style.display = 'none';
        loader.style.display = 'block';
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    toggle_loader()

    var timestamp = '?t=' + new Date().getTime();
    image.src = ''

    const formData = new FormData(form);
    formData.append('src_image', src_image.files[0]);

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData,
        });

        const json = await response.json();

        toggle_loader()

        image.src = json.src + timestamp;

        document.getElementById('download').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/download/' + json.img_id)
        document.getElementById('saveGDrive').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/send-image/' + json.img_id)
    } catch (error) {
        console.log(error)
    }
});
