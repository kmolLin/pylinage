##controlKnob
from geometry import CFLine,CFPoint 

class CControlKnobImplementation():
    def __init__(self):
        self.m_RelativePoint = CFPoint()
        self.m_Point = CFPoint()
        self.m_pElement = 0
        self.pLimit1 = 0
        self.pLimit2 = 0
        self.m_bShowOnParentSelect = False
        self.m_bSelected = False
    
    def GetPoint(self):
        Point = self.m_RelativePoint + (0 if self.m_pElement == 0 else self.m_pElement.GetLocation())
        ##change this CPoint(self.m_pElement.GetLocation())
        return Point
    
    def SetPoint(self, Point):
        Start = CFPoint()
        End = CFPoint()
        if self.GetSlideLimits( Start, End ):
            TempLine = CFLine(Start, End)
            Point.SnapToLine(TempLine,True,True)
        self.m_Point = Point
        self.m_RelativePoint =  Point-(0 if self.m_pElement == 0 else self.m_pElement.GetLocation() )
        ##change this  CPoint(self.m_pElement.GetLocation()
        return self.m_Point
        
    def SetParent(self, pElement):
        self.m_pElement = pElement
        
    def GetParent(self):return self.m_pElement
    
    def IsShowOnParentSelect(self):return self.m_bShowOnParentSelect
    
    def SetShowOnParentSelect(self, bValue):self.m_bShowOnParentSelect = bValue
    
    def SetSlideLimits(self, Point1, Point2 ):
        self.pLimit1 = Point1
        self.pLimit2 = Point2
    def GetSlideLimits(self, Point1, Point2):
        if self.pLimit1 ==0:
            return False
        Point1 = self.pLimit1.GetPoint()
        if self.pLimit2 == 0:
            Point2.SetPoint(Point1.x + 100, Point1.y + 100)
        else:
            Point2 = self.pLimit2.GetPoint()
            
        return True
        
    def Select(self, bSelect):
        self.m_bSelected = bSelect
        
    def IsSelected(self): return self.m_bSelected
    
            



class CControlKnob():
    def __init__(self):
        self.m_pImplementation = CControlKnobImplementation()
        
    def GetPoint(self):
        if self.m_pImplementation == 0:
            return CFPoint();
        return self.m_pImplementation.GetPoint()
        
    def SetPoint(self, Point):
        if self.m_pImplementation == 0:
            return CFPoint()
        return self.m_pImplementation.SetPoint(Point)
    def SetParent(self, pElement):
        if self.m_pImplementation == 0 :
            return
        self.m_pImplementation.SetParent(pElement)
        
    def GetParent(self):
        if self.m_pImplementation == 0:
            return 0
        return self.m_pImplementation.GetParent()
        
    def SetSlideLimits(self, Point1, Point2):
        if self. m_pImplementation == 0:
            return
        self.m_pImplementation.SetSlideLimits(Point1, Point2)
        
    def GetSlideLimits(self, Point1, Point2):
        if self.m_pImplementation == 0:
            return False
        return self.m_pImplementation.GetSlideLimits(Point1, Point2)
        
    def IsShowOnParentSelect(self): return self.m_bShowOnParentSelect
    
    def SetShowOnParentSelect(self, bValue):
        if self.m_pImplementation == 0:
            return
        self.m_pImplementation.SetShowOnParentSelect(bValue)
        
    def PointOnControlKnob(self, Point, TestDistance):
        if self.m_pImplementation == 0:
            return False
        OurPoint =CFPoint(self.m_pImplementation.GetPoint())
        Distance = OurPoint.DistanceToPoint(Point)
        
        return Distance <= TestDistance
        
    def Select(self, bSelect):
        self.m_bSelected = bSelect
        
    def IsSelected(self):return self.m_bSelected
    
