import json

class Data: 
    def __init__(self,userid,blog): 
        self.userid = userid
        self.blog = blog
    def __repr__(self): 
        return repr((self.userid, self.blog)) 



'''
    datas = [ 
        Data('john', 'A', 15), 
        Data('jane', 'B', 12), 
        Data('dave', 'B', 10), 
        ]
'''
def getDatas(datas):
    json_str = json.dumps(datas, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    return json_str;

