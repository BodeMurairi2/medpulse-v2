BLACK_LISTED_TOKENS = set() 

def add_to_blacklist(token: str):
    BLACK_LISTED_TOKENS.add(token)

def is_token_blacklisted(token: str) -> bool:
    return token in BLACK_LISTED_TOKENS
