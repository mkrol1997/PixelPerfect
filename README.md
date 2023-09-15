<p align="center">
<img src="pixel_perfect/pixel_perfect/static/pixel_perfect/assets/images/logo.png" width="500px" style="align=center"/>
</p>

# [PixelPerfect - Image Enhancement and Upscaling Web App](https://github.com/mkrol1997/pixel-perfect/)
[![GitHub Stars](https://img.shields.io/github/stars/mkrol1997/pixel-perfect?style=social)](https://github.com/mkrol1997/pixel-perfect/)
[![download](https://img.shields.io/github/downloads/mkrol1997/pixel-perfect/total.svg)](https://github.com/mkrol1997/pixel-perfect/releases)
![python version](https://img.shields.io/badge/python-3.11-yellow.svg)
![django version](https://img.shields.io/badge/Django-4.2.3-green.svg)
![celery version](https://img.shields.io/badge/celery-5.3.4-blue.svg)
![pytorch version](https://img.shields.io/badge/pytorch-1.7-orange.svg)
![docker version](https://img.shields.io/badge/docker-darkblue.svg) 
![License](https://img.shields.io/badge/license-Apache%202-blue.svg)


# Contents

* [Description](#Description)
* [Visual Examples](#Visual-Examples)
* [Installation](#)
* [Usage](#)
* [Citation](#)
* [License and Acknowledgement](#)
________
Description
----------

Welcome to the PixelPerfect Web App, a versatile tool that empowers users to easily transform their images. Whether you're dealing with low-resolution photos, noisy images, or compression artefacts, our web app offers a comprehensive solution to enhance, upscale, and refine your visuals.

## Key Features:

### 1. Image Upscaling

Do your low-resolution images lack the detail and clarity you need? PixelPerfect allows you to increase the resolution of your images without compromising quality. Perfect for enhancing old photographs, small thumbnails, or web graphics, this feature breathes new life into your visuals.

### 2. Artifact Removal

Eliminate unwanted image artefacts that can detract from the overall quality of your pictures. Our app employs advanced algorithms to automatically detect and remove noise, compression artefacts, and distortions, ensuring that your images look their best.

### 3. Save Locally or to Google Drive

After enhancing and upscaling your images, you have the freedom to save the edited versions in two convenient ways:
- **Local Storage:** Save images directly to your local drive for easy access and offline use.
- **Google Drive Integration:** Seamlessly sync your edited images with your Google Drive account, making them accessible from anywhere.

### 4. User Accounts

Experience enhanced convenience by creating a dedicated user account within the web app. With your account, you can effortlessly save and manage your edited images, streamlining your workflow and facilitating future downloads.

### 5. Google OAuth2 Integration

Simplify the registration and login process with our seamless Google OAuth2 integration. You can create an account or log in using your Google credentials, ensuring a secure and frictionless user experience.

Whether you're a professional photographer, a graphic designer, or someone looking to improve their personal photos, PixelPerfect provides the tools you need to transform your images into sharper, more detailed visuals effortlessly.

Ready to elevate your images and streamline your image processing workflow? Sign up today or log in with your Google account to get started!

________
# Visual Examples



________
# Installation

  ### Prerequisites
    * Python 3.9+
    * Docker Destop
  
## Installation Guide

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/your-repo.git
    ```

    Replace `your-username` with your GitHub username and `your-repo` with the name of your repository.

2. **Navigate to the Project Directory:**

    ```bash
    cd your-repo
    ```

    Replace `your-repo` with the actual name of your repository.

3. **Build and Start Containers:**

    - Make sure you have Docker and Docker Compose installed.
    
    ```bash
    docker-compose up -d
    ```

    This command runs the containers in detached mode. If you want to see the logs, omit the `-d` flag.

4. **Access the App:**

    - Once the containers are running, access the app in your web browser.
    - Open your browser and enter the app's URL, which may be something like `http://localhost:port`, depending on your app's configuration.

5. **Shutdown and Cleanup:**

    ```bash
    docker-compose down
    ```

    This will stop and remove the containers while preserving your app's data.

6. **Additional Configuration:**

    - If your app requires additional configuration, such as environment variables or specific settings, make sure to provide instructions for these in your README or a separate configuration file.

7. **Troubleshooting:**

    - If you encounter issues during the installation process, consult the troubleshooting section in your README or provide information on how users can seek help or report problems.
