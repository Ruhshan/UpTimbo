from django.forms import URLField
def url_valid(url):
    is_valid = True
    f = URLField()

    try:
        f.clean(url)
    except:
        is_valid=False
    return is_valid



def site_validator(data):
    has_error = False
    errors = {}
    if len(data['name'])==0:
        errors['name'] =  True
        has_error=True

    if url_valid(data['url'])==False:
        errors['url'] = True
        has_error = True

    data['errors']=errors
    return has_error,data
