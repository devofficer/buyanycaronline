

def convert_to_dict(args: dict):
    json = dict()
    for key, value in args.items():
        if "len" in key:
            pass
        key_vals = str(key).split("_")
        last_index = len(key_vals)
        json[str(key_vals[last_index-1])] = value
    return json




