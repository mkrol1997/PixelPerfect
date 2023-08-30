
function gallery_modal(img_src, img_title, img_id){
    document.getElementById('image-gallery').setAttribute("src", img_src)
    document.getElementById('download').setAttribute("href", 'http://localhost:8000/images/download/'+img_id)
    document.getElementById('saveGDrive').setAttribute("href", 'http://localhost:8000/images/send-image/'+img_id)

    document.getElementById('modal-title').innerText = img_title;

    $('.modal').modal('show');
    return false;
}
