
# Module to build util functions or classes

def make_upper_camel_case_names(name):
    # split name in case that name have more than one word
    names_list = name.split()
    if len(names_list) > 1:
        split_names_list = []
    # apply Upper Camel Case to string
        for name in names_list:
            modified_name = name[0].upper()+name[1:].lower()
            split_names_list.append(modified_name)
        return " ".join(split_names_list)
    return name[0].upper()+name[1:].lower()
