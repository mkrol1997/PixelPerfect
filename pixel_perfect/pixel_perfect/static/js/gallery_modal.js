
function gallery_modal(img_src, img_title, img_dwnld_url, img_gdrive_upld_url){
    document.getElementById('image-gallery').setAttribute("src", img_src)
    document.getElementById('download').setAttribute("href", 'http://localhost:8000/images/download/'+img_dwnld_url)
    document.getElementById('saveGDrive').setAttribute("href", 'http://localhost:8000/images/send-image/'+img_gdrive_upld_url)
    document.getElementById('modal-title').innerText = img_title;
    $('.modal').modal('show');
    return false;
}
