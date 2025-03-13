# AWS Cognito for drugvlab-library
## Create user pool of AWS cognito using terraform
1. Provider types: cognito user pool
2. Cognito user pool sign-in options: Email
3. Password policy mode:
	- Password minimum length
	- 8 character(s)
	- Password requirements
	- Contains at least 1 number
	- Contains at least 1 special character
	- Contains at least 1 uppercase letter
	- Contains at least 1 lowercase letter
	- Temporary passwords set by administrators expire in
	- 7 day(s)
4. MFA enforcement: optional MFA, Authenticator apps
5. Enable self-service account recovery
6. Delivery method for user account recovery messages: Email Only
7. Enable self-registration
8. Cognito-assisted verification and confirmation: Allow Cognito to automatically send messages to verify and confirm
9. Attributes to verify: Send email message, verify email address
10. Keep original attribute value active when an update is pending
11. Active attribute values when an update is pending: Email address
12. Required attributes: email
13. send email with cognito
	- ses region: seoul
14. from email address: no-reply@verificationemail.com
15. User pool name: drugvlab-library
16. Initial app client
	- App type: public client
	- App client name: drugvlab-library-app-client
	- Don't generate a client secret
	
## Create identity pool of AWS cognito using terraform
1. User access: authenticated access
2. Authenticated identity sources: Amazon cognito user pool
3. Authenticated role
	- create a new IAM role
		- role name: drugvlab-library-cognito-auth-role
4. User pool ID: The ID of the previously created cognito user pool above
5. App client ID: The ID of the previously created cognito app client above (drugvlab-library-app-client)
6. Role selection: Use default authenticated role
7. Attributes for access control: Claim mapping - inactive
8. Identity pool name: drugvlab-library