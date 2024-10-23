import pandas as pd

def parse_textgrid(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    data = {"words": [], "phones": []}
    current_tier = None
    
    for line in lines:
        line = line.strip()
        
        # Detect the current tier (words or phones)
        if 'name = "words"' in line:
            current_tier = "words"
        elif 'name = "phones"' in line:
            current_tier = "phones"
        
        # Parse intervals for the current tier
        if line.startswith('xmin'):
            xmin = float(line.split('=')[1].strip())
        elif line.startswith('xmax'):
            xmax = float(line.split('=')[1].strip())
        elif line.startswith('text'):
            text = line.split('=')[1].strip().strip('"')
            if current_tier:
                data[current_tier].append({"xmin": xmin, "xmax": xmax, "text": text})
    
    return data

def textgrid2df(textGrid_path: str):
    """
    Convert a textGrid file to a pandas DataFrame.

    assume the textGrid has 2 of IntervalTier type:
      - "words"
      - "phones"
    
    The output DataFrame has the following columns:
      - "type" ... either "word" or "phone"
      - "label" ... the word or phone label
      - "start_time" ... the start time of the word or phone in seconds
      - "end_time" ... the end time of the word or phone in seconds

    Args:
        textGrid_path (str): path to the textGrid file
    
    Returns:
        pd.DataFrame: DataFrame with columns "type", "label", "start_time", "end_time"
    """
    data = parse_textgrid(textGrid_path)
    
    words = pd.DataFrame(data["words"])
    words["type"] = "word"
    
    phones = pd.DataFrame(data["phones"])
    phones["type"] = "phone"
    
    df = pd.concat([words, phones], ignore_index=True)
    df = df[["type", "text", "xmin", "xmax"]]
    df.columns = ["type", "label", "start_time", "end_time"]
    
    return df

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Convert a TextGrid file to a pandas DataFrame.')  
    parser.add_argument('textgrid_path', type=str, help='path to the TextGrid file')
    parser.add_argument('output_path', type=str, help='path to the output csv file')
    args = parser.parse_args()

    df = textgrid2df(args.textgrid_path)
    if args.output_path == '-':
        df.to_csv(sys.stdout, index=False)
    else:
        df.to_csv(args.output_path, index=False)
