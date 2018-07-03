import pandas as pd

from ._utils import _fetch

def _normalize_data(spec):
    """Converts the data to a Pandas dataframe

    Parameters
    ----------
    spec : dict
    The vega-lite specification in json format

    Returns
    -------
    dict
    The vega-lite specification with the data format fixed to a Pandas dataframe

    Raises
    ------
    KeyError
    Raised when the specification does not contain any data attribute

    NotImplementedError
    Raised when the data specification has an unsupported data source
    """

    if not spec.get('data'):
        raise KeyError('Please specify a data source.')
    
    if spec['data'].get('url'):
        df = pd.DataFrame(_fetch(spec['data']['url']))
    elif spec['data'].get('values'):
        df = pd.DataFrame(spec['data']['values'])
    else:
        raise NotImplementedError('Given data specification is unsupported at the moment.')

    del spec['data']
    spec['data'] = df

    return spec