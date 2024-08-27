class APIKeyAuth:
    api_keys = {
        'user1': 'key1',
        'user2': 'key2'
    }

    def authenticate(self, request):
        api_key = request.headers.get('Authorization') or request.args.get('api_key')
        if not api_key or api_key not in self.api_keys.values():
            raise Exception("Invalid API key")

        return True