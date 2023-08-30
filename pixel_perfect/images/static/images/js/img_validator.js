document.getElementById('id_img_path').addEventListener('change', function() {
  var file = this.files[0];

  if (file) {
    var reader = new FileReader();
    reader.onloadend = function() {
      var image = new Image();

      image.onload = function() {
        var width = this.width;
        var height = this.height;

        if (height > width) { // Portrait Image
          if (height > 1920 || width > 1080) {
            alert("Image can't be larger than:\nLandscape: 1920x1080px\nPortrait: 1080x1920px");
          }
        } else { // Landscape Image
          if (height > 1080 || width > 1920) {
            alert("Image can't be larger than:\nLandscape: 1920x1080px\nPortrait: 1080x1920px");
          }
        }

        var fileSize = file.size / (1024 * 1024);
        if (fileSize > 3.1) {
          alert("Image can't be larger than 3Mb.");
        }

      };

      image.src = reader.result;
    };

    reader.readAsDataURL(file);
  }
});
