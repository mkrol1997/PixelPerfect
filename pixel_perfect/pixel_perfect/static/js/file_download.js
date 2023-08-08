document.getElementById ("saveGDrive").addEventListener ("click", saveImage, false);

function saveImage(){
    fetch('http://localhost:8000/send-image/', {
        method: 'GET',
        headers: {'Access-Control-Allow-Origin': '*'}
    })
    .then(res => res.json())
    .then((json) => console.log(json))
}
