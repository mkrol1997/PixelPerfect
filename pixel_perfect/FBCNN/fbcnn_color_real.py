import os.path
from collections import OrderedDict

import requests
import torch
from django.conf import settings

from FBCNN.models.network_fbcnn import FBCNN as net
from FBCNN.utils import utils_image as util


def enhance(src_image_path, cnn_model, quality_factor):
    n_channels = 3  # set 1 for grayscale image, set 3 for color image
    model_name = "fbcnn_color.pth"

    nc = [64, 128, 256, 512]
    nb = 4

    do_flexible_control = True

    model_path = cnn_model

    if not os.path.exists(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        url = "https://github.com/jiaxi-jiang/FBCNN/releases/download/v1.0/{}".format(os.path.basename(model_path))
        r = requests.get(url, allow_redirects=True)
        open(model_path, "wb").write(r.content)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    border = 0

    # ----------------------------------------
    # load model
    # ----------------------------------------

    model = net(in_nc=n_channels, out_nc=n_channels, nc=nc, nb=nb, act_mode="R")
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    for k, v in model.named_parameters():
        v.requires_grad = False
    model = model.to(device)

    test_results = OrderedDict()
    test_results["psnr"] = []
    test_results["ssim"] = []
    test_results["psnrb"] = []

    img_L = util.imread_uint(src_image_path, n_channels=n_channels)

    img_L = util.uint2tensor4(img_L)
    img_L = img_L.to(device)

    qf_input = (
        torch.tensor([[quality_factor / 100]]).cuda()
        if device == torch.device("cuda")
        else torch.tensor([[quality_factor / 100]])
    )
    img_E, QF = model(img_L, qf_input)
    QF = 1 - QF
    img_E = util.tensor2single(img_E)
    img_E = util.single2uint(img_E)
    util.imsave(img_E, src_image_path)

    return src_image_path


if __name__ == "__main__":
    ...
