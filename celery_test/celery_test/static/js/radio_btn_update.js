var scale_radio1
var scale_radio2

const radio_lapsrn = document.getElementById('id_upscale_method_3');

radio_lapsrn.addEventListener('click', function() {
    scale_radio1 = document.getElementById('id_upscale_size_1');
    scale_radio2 = document.getElementById('id_upscale_size_2');

    scale_radio1.parentElement.innerHTML = '<input type="radio" name="upscale_size" value="4" class="form-check form-check-inline" id="id_upscale_size_1" required=""> x4';
    scale_radio2.parentElement.innerHTML = '<input type="radio" name="upscale_size" value="8" class="form-check form-check-inline" id="id_upscale_size_2" required=""> x8';
});


const radios = document.getElementsByClassName('radiobtn');
const radioArray = Array.from(radios);


radioArray.forEach((radio, index) => {
  if (index < radioArray.length - 1) {
    radio.addEventListener('click', function() {
        scale_radio1 = document.getElementById('id_upscale_size_1');
        scale_radio2 = document.getElementById('id_upscale_size_2');

        scale_radio1.parentElement.innerHTML = '<input type="radio" name="upscale_size" value="3" class="form-check form-check-inline" id="id_upscale_size_1" required=""> x3';
        scale_radio2.parentElement.innerHTML = '<input type="radio" name="upscale_size" value="4" class="form-check form-check-inline" id="id_upscale_size_2" required=""> x4';

    });
  }
});