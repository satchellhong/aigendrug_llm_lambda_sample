resource "aws_cognito_identity_pool" "main" {
  identity_pool_name               = "drugvlab-library"
  allow_unauthenticated_identities = false

  cognito_identity_providers {
    provider_name     = aws_cognito_user_pool.main.endpoint
    client_id         = aws_cognito_user_pool_client.main.id
    server_side_token_check = true
  }
}

resource "aws_iam_role" "auth_role" {
  name = "drugvlab-library-cognito-auth-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity",
        Effect = "Allow",
        Principal = {
          Federated = "cognito-identity.amazonaws.com"
        },
        Condition = {
          "StringEquals": {
            "cognito-identity.amazonaws.com:aud": aws_cognito_identity_pool.main.id
          },
          "ForAnyValue:StringLike": {
            "cognito-identity.amazonaws.com:amr": "authenticated"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "auth_role_policy" {
  name   = "auth-role-policy"
  role   = aws_iam_role.auth_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "cognito-sync:*",
          "cognito-identity:*"
        ],
        Resource = "*"
      }
    ]
  })
}
