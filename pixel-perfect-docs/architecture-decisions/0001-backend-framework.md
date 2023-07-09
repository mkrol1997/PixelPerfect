# Backend Framework

Date: `2023-07-09`

## Status

`Proposed`

## Context

To upscale or improve the details of an image, it is necessary to increase its resolution. To fill in the missing pixels, it is needed to use one of the interpolation algorithms.
To achieve the best results, the solution is to use machine learning with a trained model. Because of the lack of training data, it's needed to use a framework with 
pre-trained models.

## Decision

> - What is the change that we're proposing and doing?
It is prudent to use the OpenCV framework with pre-trained models.
Including OpenCV in the project eliminates the need of collecting training data, and model training process itself.
 
## Consequences

OpenCV framework comes with defined methods containing abstract logic for interpolation algorithms.
Image quality improvement strongly depends on possibilities of the framework model.

## Keywords

- OpenCV
- Image Upscaling
- Quality
