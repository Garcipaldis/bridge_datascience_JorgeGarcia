import json

def read_json_to_dict(json_fullpath):
    """
    Read a json and return a object created from it.
    Args:
        json_fullpath: json fullpath

    Returns: json object.
    """
    try:
        with open(json_fullpath, 'r+') as outfile:
            json_readed = json.load(outfile)
        return json_readed
    except Exception as error:
        raise ValueError(error)