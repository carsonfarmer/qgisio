import webbrowser
import urllib2

try:
    import github3
    has_github = True
except ImportError:
    from json import dumps, loads
    has_github = False

MAX_URL_LEN = 150e3  # Size threshold above which a gist is created

def to_geojsonio(contents, domain='http://geojson.io/'):
    url = geojsonio_url(contents, domain)
    webbrowser.open(url)

def geojsonio_url(contents, domain='http://geojson.io/'):
    """
    Returns the URL to open given the domain and contents

    If the contents are large, then a gist will be created.

    """
    if len(contents) <= MAX_URL_LEN:
        url = _data_url(domain, contents)
    else:
        url = _create_gist(contents)
    return url


def _create_gist(contents, description='', filename='data.geojson', domain='http://geojson.io/'):
    """
    Create and return an anonymous gist with a single file and specified contents
    """
    if has_github:
        ghapi = github3.GitHub()
        files = {filename: {'content': contents}}
        gist = ghapi.create_gist(description, files)
        url = _gist_url(domain, gist.id)
    else:
        new_url = 'https://api.github.com/gists'

        data = {"public": True, "files": {filename: {'content': contents}}, 
                "description": description}
        if description != '':
            data['description'] = description
        req = urllib2.Request(new_url)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req, dumps(data))
        r = loads(resp.read())
        url = _gist_url(domain, r['url'][r['url'].rfind('/')+1:])
            
    return url

def _data_url(domain, contents):
    url = (domain + '#data=data:application/json,' +
           urllib2.quote(contents))
    return url


def _gist_url(domain, gist_id):
    url = (domain + '#id=gist:/{}'.format(gist_id))
    return url


