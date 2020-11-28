import pandas as pd


def check_is_number(input_value: str) -> bool: 
    if type(input_value) == int: 
        return True
    if input_value.isnumeric():
        return True

    # Do this in case the input value is float as string
    try: 
        result = float(input_value)
        return True
    except: 
        return False


def basic_preprocess(input_data: str): 
    """ Transform the original dataframe

        Basic steps:
            1. Fill N/A
            2. Replace unknown with -1

        Args: 
            input_data: pd.DataFrame
                The dataframe you want to transform
        Returns:
            pd.DataFrame: The result dataframe
    """
    df: pd.DataFrame = input_data.copy()

    df.fillna('0', inplace=True) 
    df = df.replace('unknown', '-1')
    
    # Unnecessary string
    elements = ['like', 'comment', 'share']
    regex_pattern = r'\d+ {}'
    repl = lambda m: m.group(0).split()[0]

    for i in elements: 
        # Remove the unnecessary element 
        df[f'num_{i}_post'] = df[f'num_{i}_post'].astype(str)
        df[f'num_{i}_post'] = df[f'num_{i}_post'].str.replace(regex_pattern.format(i), repl)
        
        # Transform other to -1
        indexing_non_number = df[f'num_{i}_post'].apply(lambda x: check_is_number(x))
        false_indexes = indexing_non_number[indexing_non_number == False].index 

        for j in false_indexes: 
            df.at[j, f'num_{i}_post'] = '-1'
            df[f'num_{i}_post'] = df[f'num_{i}_post'].astype(float) 
    return df