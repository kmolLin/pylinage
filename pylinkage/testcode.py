from geometry import *
from Connector import *
from link import *
from ControlKnob import *

if __name__ == '__main__':
    a = CFPoint(10, 10)
    b = CFPoint(15, 15)
    e = CFLine(a, b)
    c = a+b
    Z = LinkList()
    f = CLink()
    #print(c.x, c.y)
    
    d = CFCircle(c, 10.)
    linkk = CLink()
    
    h = CConnector()
#    linkk.AddConnector(h)
    linkk.UpdateControlKnob(c)
    linkk.GetLocation()
    print(f.GetControlKnob())

