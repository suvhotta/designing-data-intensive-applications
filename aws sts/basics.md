## What is AWS Security Token Service?
- It is an aws service that allows to request temporary limited time credentials for 
    cross account resource access.
- It's not available on the AWS GUI, and can be only accessed programmatically.
- These temporary credentials consist of an access key ID, a secret access key, and a security token.


## assume role:
- to assume role we need to pass 2 mandatory fields: RoleArn, RoleSessionName.
- RoleArn: its the arn of the role we wish to assume.
- RoleSessionName: its the identifier for the assumed role session. Use the role session name to 
  uniquely identify a session when the same role is assumed by different principals or for different reasons.
- The role is to first created by the account whose resources we want to access.
- the best practice is to have the role added to the role policy of the aws resource which will be assuming
    the role(the consumer). Also in the role policy of the publisher, in the trust relationships, its useful to
    specify the aws roots that will be assuming role from the consumer side.
- 