from misc import Failure

class Vector(object):
    def __init__(self,arg):
        if isinstance(arg,int) or isinstance(arg,long):
            if arg>=0:
                self.v_list = [0.0 for i in range(arg)]
            else:
                raise ValueError("Vector length cannot be negative")
        elif hasattr(arg, "__getitem__") or hasattr(arg,"__iter__"):
            self.v_list = [x for x in arg]                #Needs to be updated to include other sequences
        else:
            raise TypeError("Not a valid argument type")
    
    def __repr__(self):
        return "Vector("+str(self.v_list)+")"
    
    def __len__(self):
        return len(self.v_list)
    
    def __iter__(self):
        return iter(self.v_list)
    
    def __add__(self, value):
        return Vector([v1+v2 for v1,v2 in zip(self.v_list,value)])
    
    def __radd__(self, value):
        return Vector([v1+v2 for v1,v2 in zip(self.v_list,value)])
        
    def __iadd__(self, value):
        return Vector([v1+v2 for v1,v2 in zip(self.v_list,value)])
    
    def dot(self,l):
        try:
            num = 0
            for v1,v2 in zip(self.v_list,l):
                num = num + (v1 * v2)
            return num
        except (TypeError):
            raise TypeError("Argument must be a vector or sequence")
    
    def __getitem__(self, key):
        try:
            return self.v_list[key]
        except (IndexError):
            raise IndexError("Vector index out of range")
    
    def __setitem__(self, key, value):
        new_list = self.v_list[:]
        try:
            new_list[key] = value
            if len(new_list) <> len(self.v_list): raise ValueError("Vector length cannot be changed")
            else: self.v_list = new_list
        except (IndexError):
            raise IndexError("Vector index out of range")
    
    def __eq__(self, vec):
        if vec.__class__ <> Vector: return False
        if self.v_list == vec.v_list: return True
        else: return False
            
    def __lt__(self, vec):
        if vec > self: return True
        else: return False
    
    def __le__(self, vec):
        if self.eq_sorted(vec) or vec > self: return True
        else: return False
    
    def __ne__(self, vec):
        if self == vec: return False
        else: return True
    
    def __gt__(self, vec):
        if vec.__class__ <> Vector: return False
        sorted1 = self.v_list[:]
        sorted2 = vec.v_list[:]
        sorted1.sort(reverse=True)
        sorted2.sort(reverse=True)
        for v1,v2 in zip(sorted1,sorted2):
            print v1,v2
            if v1 > v2: return True
        if len(sorted1)>len(sorted2): return True
        return False
    
    def __ge__(self, vec):
        if self > vec or self.eq_sorted(vec): return True
        else: return False
        
    def eq_sorted(self,vec):
        if len(self) <> len(vec): return False
        sorted1 = self.v_list[:]
        sorted2 = vec.v_list[:]
        sorted1.sort(reverse=True)
        sorted2.sort(reverse=True)
        for v1,v2 in zip(sorted1,sorted2):
            if v1 != v2: return False
        return True
 