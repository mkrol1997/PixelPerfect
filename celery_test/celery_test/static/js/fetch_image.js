const image = document.getElementById("new-image");
const form = document.getElementById('image_form');
const src_image = document.querySelector('#id_img_path');

const content = document.getElementById('image-modal')
const loader = document.getElementById('loader')

const submitBtn = document.getElementById('submit');
const resultBtn = document.getElementById('toggleModal');

function show_modal(){
    $('.modal').modal('show');
}

function toggle_loader(){
    if (content.style.display == 'none') {
        content.style.display = 'block';
        loader.style.display = 'none';
    }
    else {
        content.style.display = 'none';
        loader.style.display = 'block';
    }
}

function fetch_image(task_id) {
	setTimeout(async function() {
		get_status_api = window.location.protocol + '//' + window.location.host + '/track/?task_id=' + task_id;

		let response = await fetch(get_status_api);
		let json_response = await response.json();
        console.log(json_response.status)
		if(json_response.status == 'SUCCESS') {
		    var timestamp = '?t=' + new Date().getTime();

            toggle_loader()

            image.src = json_response.result.src + timestamp;
            document.getElementById('download').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/download/' + json_response.result.id);
            document.getElementById('saveGDrive').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/send-image/' + json_response.result.id)

            submitBtn.disabled = false;
			return;
		}

		fetch_image(task_id);
	}, 1000);
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    toggle_loader()
    image.src = ''

    resultBtn.removeAttribute("disabled");
    submitBtn.disabled = true;

    const formData = new FormData(form);
    formData.append('src_image', src_image.files[0]);

    try {
        const response = await fetch(window.location.href, {
            method: 'POST',
            body: formData,
        });

        const upscale_task = await response.json();
        await fetch_image(upscale_task.task_id)

    } catch (error) {
        console.log(error)
    }
});

