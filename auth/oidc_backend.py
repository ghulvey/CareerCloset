import requests
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CareerClosetOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    # Get user info from Microsoft Entra using the access token
    def get_userinfo(self, access_token, id_token, payload):
        headers = {
            'Authorization': f'Bearer {access_token}',
        }
        response = requests.get('https://graph.microsoft.com/oidc/userinfo', headers=headers)

        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            raise Exception('Failed to fetch user info from Azure AD')

    def create_user(self, claims):
        user = super(CareerClosetOIDCAuthenticationBackend, self).create_user(claims)
        user.save()
        return user

    def get_or_create_user(self, access_token, id_token, payload):
        user = super().get_or_create_user(access_token, id_token, payload)

        # If the user is a staff member, update their information based on Microsoft Entra
        if user.is_staff:
            user_info = self.get_userinfo(access_token, id_token, payload)
            if user_info.get('givenname'):
                user.first_name = user_info.get('givenname', '')
            if user_info.get('given_name'):
                user.first_name = user_info.get('given_name', '')
            if user_info.get('familyname'):
                user.last_name = user_info.get('familyname', '')
            if user_info.get('family_name'):
                user.last_name = user_info.get('family_name', '')
        user.save()
        return user
