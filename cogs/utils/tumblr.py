import requests
from requests.exceptions import HTTPError
class Client:

    def __init__(self, key, blogname=None):
        self.host = 'https://api.tumblr.com'
        self.base_url = self.host + '/v2/blog/'
        self.base_url += blogname + '/' if blogname else ''
        self.key = key  

    def get(self, method='info', **params):
        type = params.get('type')
        url = self.base_url + method + ('/' + type) if type else ''
        params['api_key']=self.key
        return requests.get(url, params=params).json()
   
    def info(self):
        return self.get('info')
    
    def total_posts(self, **params):
        return self.posts(**params)['total_posts']
    
    def total_photos(self, **params):
        return self.posts(type='photo', **params)['total_posts']
        
    def posts(self, **params):
        posts = self.get(method='posts', **params)
        if not posts['response']:
            raise HTTPError(posts['meta']['status'], posts['meta']['msg'])
        return posts['response']
        
    def photos(self, **params):
        return self.posts(type='photo', **params)



            

    
