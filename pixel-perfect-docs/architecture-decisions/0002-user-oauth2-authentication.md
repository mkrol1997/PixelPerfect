# User authentication

Date: `2023-07-09`

## Status

`Proposed`

## Context

Most of the sites require users to create dedicated accounts to use a website's functionalities.
The common user register method involves a need of choosing a unique username, creating a new password, 
and verifying an account via email link etc.

## Decision

Implementing OAuth2 authentication using Gmail allows to authenticate users without the necessity of creating a dedicated account. 

The vast majority of Internet users have an active Gmail account, which they can use to authenticate on a website 
without having to go through the registration stage.
 
## Consequences

Simpler and faster authentication can be reached with the OAuth2 framework.
Authentication depends on external service servers.
Database size will grow faster as more fields need to be stored for each user.

## Keywords

- Oauth
- Login
- Authentication
- Authorization
- Gmail
