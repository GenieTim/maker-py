import re


def clean_variable_name(s):

   # Remove invalid characters
   s = re.sub('[^0-9a-zA-Z_]', '', s)

   # Remove leading characters until we find a letter or underscore
   s = re.sub('^[^a-zA-Z_]+', '', s)

   return s

