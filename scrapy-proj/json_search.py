# "family_name": "HEYDAROV")
# print(json.dumps(my_json, indent=4))
def json_find_tree(my_json , key, val) :
    
    if isinstance(my_json, list):
        for index in range(len(my_json)):
            
            res = json_find_tree( my_json[index], key, val )
            if res:
                return [index] + res       
    
    elif isinstance(my_json, dict):
        
        for (k, v) in my_json.items():
            if (k, v) == (key, val):
                return [key]
            
            res = json_find_tree( my_json[k], key, val )
            if res:
                return [k] + res 
            
    else:
        return None
        
    return None

# print( json_find_tree(my_json, "family_name", "HEYDAROV")  )