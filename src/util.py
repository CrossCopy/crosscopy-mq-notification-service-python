def construct_signup_email_verification_redis_key(username: str, email: str, code: str):
    return f"signup:email-verification:{username}:{email}:{code}"

