import pandas as pd
import os

def combine_excel_sheets(file_path, output_sheet_name='Combined_Data'):
    """
    Combines all sheets from an Excel workbook into one DataFrame 
    and adds a column with the original sheet name.

    Args:
        file_path (str): The path to the source Excel file.
        output_sheet_name (str): The name for the combined sheet in the output file.
    """
     # Define the sheet name to skip
    sheet_to_skip = "Attribute mappings"
    
    df_header = pd.read_excel(file_path, sheet_name=sheet_to_skip, header=5)
    # Read all sheets from the Excel file into a dictionary of DataFrames
    # The keys of the dictionary will be the sheet names.
    all_dfs = pd.read_excel(file_path, sheet_name=None, header=4)
    
    # Create an empty list to store the modified DataFrames
    df_list = []
    df_list.append(df_header)
    
    # Iterate through the dictionary items (sheet_name and DataFrame)
    for sheet_name, df in all_dfs.items():
        # Add a new column named 'Source Sheet' with the current sheet's name
        if sheet_name == sheet_to_skip:
            continue
        text = sheet_name.split('_', 1)
        df['ECU'] = text[0]
        df['Baseline'] = text[1]
        df_list.append(df)
    
    # Concatenate all DataFrames in the list into one single DataFrame
    # ignore_index=True resets the index for the final combined DataFrame
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Define the output file path (adds '_combined' to the original filename)
    base, ext = os.path.splitext(file_path)
    output_file_path = f"{base}_combined{ext}"
    
    # Write the combined DataFrame to a new Excel file
    # Use the specified output_sheet_name for the single sheet
    combined_df.to_excel(output_file_path, sheet_name=output_sheet_name, index=False)
    
    print(f"Successfully combined all sheets into '{output_file_path}' in the '{output_sheet_name}' sheet.")
    return combined_df
