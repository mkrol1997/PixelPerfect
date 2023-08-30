const radio_btns = document.querySelectorAll('label:has(input[type="radio"])');
const img_input = document.getElementById('id_img_path')

function disableField() {
    const invalidForm = document.querySelector('form:invalid');
    const submitBtn = document.getElementById('submit');

    if (resultBtn.hasAttribute('disabled')){
        if (invalidForm) {
        submitBtn.disabled = true;
        } else {
           submitBtn.disabled = false;
        }
    }
}

img_input.addEventListener('change', disableField);

radio_btns.forEach((btn) => {
    btn.addEventListener('change', disableField);
});
