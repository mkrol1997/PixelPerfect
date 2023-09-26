# ADR: Artifact Removal Using FBCNN Module

Date: `2023-07-07`

## Status

`Accepted`

## Context

In our project, users should be able to restore old images with image artifacts removal. To address this issue, we propose implementing the FBCNN (Fast Blind Convolutional Neural Network) module, which is an open-source and effective solution for artifact removal.

## Decision

We propose the implementation of the FBCNN module for artifact removal in our image enhancement pipeline. This decision involves the following steps:

1. **FBCNN Integration**: We will integrate the FBCNN module to perform artifact removal.

2. **Preprocessing**: Input images will be preprocessed to prepare them for artifact removal, including resizing and format conversion.

3. **Artifact Detection**: FBCNN will be used to detect and identify artifacts in the input images. It will analyze image regions for potential artifacts.

4. **Artifact Removal**: Detected artifacts will be removed or reduced using the FBCNN module, resulting in enhanced images with improved quality.

Implementing the FBCNN module for artifact removal aligns with our goal of providing high-quality image enhancement features to our users.

## Consequences

### Positive Consequences

- **Improved Image Quality**: Implementing the FBCNN module will significantly improve the quality of enhanced images by effectively removing artifacts.

- **Enhanced User Experience**: Users will benefit from the removal of artifacts, resulting in more visually appealing and usable images.

- **Open Source Solution**: FBCNN is an open-source solution, allowing us to leverage community contributions and updates for continuous improvement.

### Negative Consequences

- **Integration Complexity**: Integrating the FBCNN module introduces additional complexity into our image processing application, which may require additional development and testing effort.

- **Performance Considerations**: The artifact removal process using FBCNN may have an impact on processing time, especially for larger images.

- **Fine-tuning**: Fine-tuning and optimizing the FBCNN module for our specific use case may be necessary to achieve the desired results.

## Keywords

- FBCNN
- Artifact Removal
- Image Enhancement
- Open Source
- Quality Improvement
- User Experience