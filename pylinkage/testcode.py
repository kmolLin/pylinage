from geometry import *
from Connector import *
from link import *

if __name__ == '__main__':
    a = CFPoint(10, 10)
    b = CFPoint(15, 15)
    e = CFLine(a, b)
    c = a+b
    #print(c.x, c.y)
    
    d = CFCircle(c, 10.)
    linkk = CLink()
    '''
    h = CConnector()
    linkk.AddConnector(h)
    
    print(a.x)
    print(e.GetAngle())
    '''
    print(d.GetCenter())
