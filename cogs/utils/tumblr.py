import requests

class Client:

    def __init__(self, key, blogname=None):
        self.host = 'https://api.tumblr.com'
        self.base_url = self.host + '/v2/blog/'
        self.base_url += blogname + '/' if blogname else ''
        self.key = key  

    def get(self, method='info', **params):
        url = (self.base_url + method
               + ('/' + params.get("type") if params.get('type') else ''))
        params['api_key']=self.key
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()['response']
   
    def info(self):
        return self.get('info')
    
    def total_posts(self, **params):
        return self.posts(**params)['total_posts']
    
    def total_photos(self, **params):
        return self.posts(type='photo', **params)['total_posts']
        
    def posts(self, **params):
        return self.get(method='posts', **params)
        
    def photos(self, **params):
        return self.posts(type='photo', **params)



            

    
