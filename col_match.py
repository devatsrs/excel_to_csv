import sys
from fuzzywuzzy import process
import json
from urllib.parse import unquote


if __name__ == '__main__':
    # argument for souce filename
    # argument for destination filename
    str2Match = sys.argv[1]
    # ["Products", "description", "msrp", "dealer price", "map price"]
    strOptions = unquote(sys.argv[2]).split(",")


# print(sys.argv)
# print(strOptions)
# print(strOptions)
# str2Match = "dealer"
# strOptions = ["Products", "description", "msrp", "dealer price", "map price"]
Ratios = process.extract(str2Match, strOptions)
# print(Ratios)
# You can also select the string with the highest matching percentage
highest = process.extractOne(str2Match, strOptions)
# print(highest)
print(json.dumps(highest))
