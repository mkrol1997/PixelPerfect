function gallery_modal(img_src, img_title, img_id){
    document.getElementById('image-gallery').setAttribute("src", img_src)
    document.getElementById('download').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/download/' +img_id)
    document.getElementById('saveGDrive').setAttribute("href", window.location.protocol + '//' + window.location.host + '/images/send-image/'+img_id)
    document.getElementById('imgDeleteForm').setAttribute('action', window.location.protocol + '//' + window.location.host + '/images/delete-image/?img_id='+img_id)

    document.getElementById('modal-title').innerText = img_title;

    $('.modal').modal('show');
    return false;
}
