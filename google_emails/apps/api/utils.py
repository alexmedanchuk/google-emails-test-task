import httplib2

import oauth2client
import apiclient


class EmailsRetriever(object):
    """Used to retrieve emails list from gmail API.

    Takes 2 arguments:
    access_token - access token to create google API client credentials object,
    user_id - email of user to retrieve mails.
    """

    FIELDS_TO_RETRIEVE = ('Subject', 'Date', 'Reply-To', 'From')
    MAX_RESULTS = 100

    def __init__(self, access_token, user_id):
        self._credentials = oauth2client.client.AccessTokenCredentials(access_token, '')
        self._http = self._credentials.authorize(httplib2.Http())
        self._user_id = user_id

    def _get_mails_list(self):
        service = apiclient.discovery.build('gmail', 'v1', http=self._http)
        return service.users().messages().list(
            userId=self._user_id,
            maxResults=self.MAX_RESULTS,
            q='to:{}'.format(self._user_id)
        ).execute()

    def _handle_batch(self, request_id, response, exception):
        if exception is not None:
            pass
        else:
            for message in self._messages:
                if message['id'] == request_id:
                    data = {
                        'snippet': response['snippet']
                    }
                    for header in response['payload']['headers']:
                        if header['name'] in self.FIELDS_TO_RETRIEVE:
                            data.update({ header['name']: header['value']})
                    message['data'] = data
            # print(response)

    def retrieve(self):
        response = self._get_mails_list()
        self._messages = response['messages']
        service = apiclient.discovery.build('gmail', 'v1')
        batch = service.new_batch_http_request(callback=self._handle_batch)

        for message in self._messages:
            batch.add(service.users().messages().get(userId=self._user_id, id=message['id']), request_id=message['id'])

        batch.execute(http=self._http)
        return self._messages
