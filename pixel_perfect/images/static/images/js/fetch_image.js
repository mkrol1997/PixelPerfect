const image = document.getElementById("new-image");
const form = document.getElementById('image_form');
const src_image = document.querySelector('#id_img_path');
const submitBtn = document.getElementById('submit');
const resultBtn = document.getElementById('toggleModal');

const invalid_form_msg = `
    <div class="d-block-flex align-items-center" style="width: fit-content;">
        <p>Something went wrong. Make sure that:</p>
        <ul>
            <li>Supported file extensions: .jpg, .jpeg, .png</li>
            <li>Image size does not extend: 3Mb</li>
            <li>Image dimensions do not extend:
                <div class="container text-center">
                    <ul>
                        <li>Landscape: 2400x1440px</li>
                        <li>Portrait: 1440x2400px</li>
                        <li>Square: 1440x1440px</li>
                    </ul>
                </div>
            </li>
        </ul>
    </div>
`;

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
    console.log(src_image.files[0])
    document.getElementById('messageContainer').setAttribute("style", "display: none");

    toggle_loader()

    var timestamp = '?t=' + new Date().getTime();
    image.src = ''

    const formData = new FormData(form);

    try {
        resultBtn.disabled = false;
        submitBtn.setAttribute('disabled', true)
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData,
        });

        const json = await response.json();

        if (json.form_valid) {

            toggle_loader()

            image.src = json.src + timestamp;

            document.getElementById('download').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/download/' + json.img_id)
            document.getElementById('saveGDrive').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/send-image/' + json.img_id)
            submitBtn.disabled = false;
        } else {
            localStorage.setItem('formNotValid', 'true');
            location.reload();
        }
    } catch (error) {
        console.log(error)
    }
});

window.onload = function() {
    if (localStorage.getItem('formNotValid')) {
        document.getElementById('messageContainer').setAttribute("style", "display:block");
        document.getElementById('message').innerHTML = invalid_form_msg;

        localStorage.removeItem('formNotValid');
    }
};
