# ADR: Save Enhanced Images Locally and on Google Drive

Date: `2023-08-03`

## Status

`Accepted`

## Context

In our project, we are developing a feature that allows users to enhance their images with various filters and adjustments. Currently, users can save their enhanced images locally on their devices. However, to improve user experience and provide a convenient backup solution, we propose implementing the ability to save enhanced images not only locally but also on Google Drive.

## Decision

We propose the implementation of a feature that allows users to save their enhanced images both locally and on Google Drive. This decision involves the following steps:

1. **Google Drive Integration**: We will integrate Google Drive API into our application to facilitate interactions with Google Drive.

2. **User Authentication**: Users will be required to authenticate with their Google accounts to enable the Google Drive saving feature.

3. **Save Options**: When a user chooses to save an enhanced image, they will have the option to select whether they want to save it locally or on Google Drive, or both.

4. **Folder Management**: Application will create a directory automatically on their Google Drive, where the enhanced images will be saved.

5. **Error Handling**: We will implement error handling to address scenarios where saving to Google Drive may fail due to connectivity issues or other factors.

This decision will enhance user experience by providing a convenient cloud-based storage solution while still allowing users to retain copies of their enhanced images locally.

## Consequences

### Positive Consequences

- **Convenience**: Users will have the convenience of saving their enhanced images on Google Drive, enabling easy access and backup from any device.

- **Data Redundancy**: Saving images both locally and on Google Drive provides redundancy and data safety in case of device loss or failure.

- **User Engagement**: Offering cloud-based storage may increase user engagement and retention.

### Negative Consequences

- **Development Complexity**: Integrating Google Drive and managing user authentication can introduce additional complexity into the application.

- **User Education**: Users may need guidance on how to use the Google Drive saving feature, requiring additional documentation or support.

- **Privacy Concerns**: Users may have concerns about data privacy and security when using cloud-based storage, necessitating robust security measures.

## Keywords

- Google Drive Integration
- Enhanced Images
- Cloud Storage
- User Experience
- Redundancy
- Data Backup
- Privacy and Security