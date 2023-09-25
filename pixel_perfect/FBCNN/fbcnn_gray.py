import os
from collections import OrderedDict

import cv2
import requests
import torch
from django.conf import settings

from FBCNN.models.network_fbcnn import FBCNN as net
from FBCNN.utils import utils_image as util


def enhance(src_image_path, cnn_model, quality_factor):
    n_channels = 1  # set 1 for grayscale image, set 3 for color image
    model_name = "fbcnn_gray.pth"
    nc = [64, 128, 256, 512]
    nb = 4
    show_img = False  # default: False

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

    if n_channels == 3:
        img_L = cv2.cvtColor(img_L, cv2.COLOR_RGB2BGR)
    _, encimg = cv2.imencode(".jpg", img_L, [int(cv2.IMWRITE_JPEG_QUALITY), 100 - quality_factor])
    img_L = cv2.imdecode(encimg, 0) if n_channels == 1 else cv2.imdecode(encimg, 3)
    if n_channels == 3:
        img_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2RGB)
    img_L = util.uint2tensor4(img_L)
    img_L = img_L.to(device)

    # ------------------------------------
    # (2) img_E
    # ------------------------------------

    # img_E,QF = model(img_L, torch.tensor([[0.6]]))
    img_E, QF = model(img_L)
    QF = 1 - QF

    img_E = util.tensor2single(img_E)
    img_E = util.single2uint(img_E)
    img_H = util.imread_uint(src_image_path, n_channels=n_channels).squeeze()
    # --------------------------------
    # PSNR and SSIM, PSNRB
    # --------------------------------

    psnr = util.calculate_psnr(img_E, img_H, border=border)
    ssim = util.calculate_ssim(img_E, img_H, border=border)
    psnrb = util.calculate_psnrb(img_H, img_E, border=border)
    test_results["psnr"].append(psnr)
    test_results["ssim"].append(ssim)
    test_results["psnrb"].append(psnrb)

    util.imsave(img_E, src_image_path)

    return src_image_path


if __name__ == "__main__":
    main()
