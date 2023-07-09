# Storage of edited images

Date: `2023-07-09`

## Status

`Proposed`

## Context

Images should be stored for further access, rather than deleted right after the user leave the website.
Permanent storage of high-resolution images requires lots of storage memory.

## Decision

Images should be stored on the website server for a set amount of time.
Users authenticated with OAuth2 should be able to permanently save images on Google Drive.

## Consequences

Images storage will not require large dedicated memory as they will be removed from
the server after the expiration time.
Permanent storage available only for OAuth2 authenticated users.

## Keywords

- Storage
- Expiry time
