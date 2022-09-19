# # importing pandas as pd
# import pandas as pd

# # read an excel file and convert
# # into a dataframe object
# df = pd.DataFrame(pd.read_excel(
#     "./excel/CAV DEALER - 7-26-22 New Price Sheet for Distribution.xlsx"))

# # show the dataframe
# df

"""
# a list contains both even and odd numbers. 
seq = [0, 1, 2, 3, 5, 8, 13]
  
# result contains odd numbers of the list
result = filter(lambda x: x % 2 != 0, seq)
print(list(result))
  
# result contains even numbers of the list
result = filter(lambda x: x % 2 == 0, seq)
print(list(result))



from re import match
list_array = ["__1__","__2__","__3__","test"]
filtered_values = list(filter(lambda col: match('^__\d+__$', col) , list_array))
print(len(filtered_values))
"""

def should_skip_sheet(sheet_name):
    skip_sheets_list = [
            "Legal",  # Shure
            "Terms and Conditions",
            "Overview",
            "Navigation", # Leon-PriceGuide-COMM-2021-DLR
            "Cover" # B-Tech AV Mounts LLC Price List 2021 (Release 1.0) - Sapphire Partner
            "Cover", "T of C", "How to Spec","P.O.'s", "Demo", "Freight", "Service",   "Warranty", "DP Contacts",  #
        ]

    for word in skip_sheets_list:
        if word.lower().strip() in sheet_name.lower():
            return True

    return False

result = "Found" if should_skip_sheet("9. Demo, Freight and Services") else "No"
print(result)

