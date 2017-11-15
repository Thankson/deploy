import sys,os,time
import ConfigParser

class Config:
    def __init__(self, path):
        self.path = path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)
    def get(self, field, key):
        result = ""
        try:
            result = self.cf.get(field, key)
        except:
            result = ""
        return result
    def set(self, field, key, value):
        try:
            self.cf.set(field, key, value)
            self.cf.write(open(self.path,'w'))
        except Exception,e:
            print e
            return False
        return True
    def delete_user(self, name):
        secs = self.cf.sections()
        for sec in secs:
            if sec == 'groups':
                group_items = self.cf.items(sec)
                for k, v in group_items:
                    if ',' in v:
                        val = v.replace(',%s,'%name, ',')
                        if val.startswith('%s,'%name):
                            val = v.replace('%s,'%name, '')
                        elif val.endswith(',%s'%name):
                            val = v.replace(',%s'%name, '')
                        else:
                            pass
                        # val = val.rstrip(',%s'%name).lstrip('%s,'%name)
                        self.set(sec, k, val)
                    else:
                        if v == name:
                            val = ''
                            self.set(sec, k, val)
            else:
                group_items = self.cf.items(sec)
                for k, v in group_items:
                    if k == name:
                        self.cf.remove_option(sec, k)
                        self.cf.write(open(self.path,'w'))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    config_file_path = sys.argv[1] 
    cf = Config(config_file_path)
    if len(sys.argv) == 4:
        field = sys.argv[2]
        key = sys.argv[3]
        print cf.get(field, key)
    elif len(sys.argv) == 5:
        field = sys.argv[2]
        key = sys.argv[3]
        value = sys.argv[4]
        print cf.set(field, key, value)
    elif len(sys.argv) == 3:
        name = sys.argv[2]
        cf.delete_user(name)
    else:
        pass

# python cp.py authz.conf section option  value zengqingwen
# if delete name ;then:  python cp.py authz.conf zengqingwen
