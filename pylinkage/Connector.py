##Connector.py
MAX_DRAWING_POINTS = 600
from math import *
from Element import CElement
from geometry import CFPoint, CFLine, Distance
class ConnectorListOperation():
    def __init__(self):
        pass
    def truth(self, pConnector,bFirst,bLast): return True

        
class ConnectorList(list):
    def __init__(self):
        pass

    def Iterate(self, Operation):

        Position = self[0]
        bFirst = True
        while( Position != 0 ):
            pConnector = CConnector(self[Position+1])
            if pConnector == 0:
                continue
            if not Operation(pConnector, bFirst, pConnector == 0):
                return False
            bFirst = False
        return True
    def Remove(self, pConnector):
        Position = self[0]
        while  Position != 0:
            RemovePosition = Position
            pCheckConnector = self[Position+1]
            if pCheckConnector != 0 and ( pConnector == 0 or pCheckConnector == pConnector ):
                self.pop(RemovePosition)
                return True
        return False
        
    def Find(self, pConnector):
        Position = self[0]
        while( Position != 0 ):
            RemovePosition = Position
            pCheckConnector = self[Position+1]
            if( pCheckConnector != 0 and ( pConnector == 0 or pCheckConnector == pConnector)):
                return pConnector
        return 0
    
class CConnector(CElement):
    def __init__(self, *keyword):
        if len(keyword)==0:
            self.Reset()
        elif len(keyword)==1:
            ExistingConnector = keyword[0]
            self.Reset()
            self.m_Point = ExistingConnector.m_OriginalPoint
            self.m_RotationAngle = ExistingConnector.m_RotationAngle
            self.m_TempPoint = ExistingConnector.m_OriginalPoint
            self.m_TempRotationAngle = ExistingConnector.m_TempRotationAngle
            self.m_OriginalPoint = ExistingConnector.m_OriginalPoint
            self.m_Identifier = ExistingConnector.m_Identifier
            self.m_RPM = ExistingConnector.m_RPM
            self.m_bInput = ExistingConnector.m_bInput
            self.m_bAnchor = ExistingConnector.m_bAnchor
            self.m_bSelected = ExistingConnector.m_bSelected
            self.m_bTempFixed = ExistingConnector.m_bTempFixed
            self.m_bDrawingConnector = ExistingConnector.m_bDrawingConnector
            self.m_Layers = ExistingConnector.m_Layers
            self.m_PreviousPoint = ExistingConnector.m_PreviousPoint
            self.m_RotationAngle = ExistingConnector.m_RotationAngle
            self.m_OriginalDrawCircleRadius = ExistingConnector.m_OriginalDrawCircleRadius
            self.m_OriginalSlideRadius = ExistingConnector.m_OriginalSlideRadius
            self.m_StartPoint = 0
            self.m_PointCount = 0
            self.m_DrawingPointCounter = 0
                    
            
    def Reset(self, *keyword):
        if len(keyword) ==0:
            self.m_Point=CFPoint()
            self.m_OriginalPoint=CFPoint()
            self.m_TempPoint=CFPoint()
            self.m_PreviousPoint=CFPoint()
            self.m_Point.x = 0
            self.m_Point.y = 0
            self.m_OriginalPoint.x = 0
            self.m_OriginalPoint.y = 0
            self.m_TempPoint.x = 0
            self.m_TempPoint.y = 0
            self.m_RotationAngle = 0.0
            self.m_TempRotationAngle = 0.0
            self.m_Identifier = 0
            self.m_bInput = False
            self.m_bAnchor = False
            self.m_bTempFixed = False
            self.m_bDrawingConnector = False
            self.m_bAlwaysManual = False
            self.m_RPM = 0
            self.m_StartPoint = 0
            self.m_PointCount = 0
            self.m_DrawingPointCounter = 9999
            #self.m_pSlideLimits = CConnector()
            #self.m_pSlideLimits[0] = 0.
            #self.m_pSlideLimits[1] = 0.
            self.m_DrawCircleRadius = 0
            self.m_OriginalDrawCircleRadius = 0
            self.m_SlideRadius = 0
            self.m_OriginalSlideRadius = 0
            self.m_Color = [ 200, 200, 200 ]
            #self.UpdateControlKnob()
        elif len(keyword) ==1:
            self.m_Point = self.m_OriginalPoint
            self.m_PreviousPoint = self.m_OriginalPoint
            self.m_RotationAngle = 0.0
            self.m_TempRotationAngle = 0.0
            self.SetPositionValid( True )
            if keyword[0]:
                self.m_StartPoint = 0
                self.m_PointCount = 0
                self._DrawingPointCounter = 9999
    
    def IsLink(self): return False
    def IsConnector(self): return True
    def GetLocation(self):return self.m_Point
    def SetPoint(self, *keyword):
        if len(keyword)==1:
            self.m_Point = keyword[0]
            self.m_OriginalPoint = keyword[0]
        elif len(keyword)==2:
            self.m_Point.x = keyword[0]
            self.m_Point.y = keyword[1]
            self.m_OriginalPoint = self.m_Point
    def SetIntermediatePoint(self, Point): self.m_Point = Point
    def MovePoint(self, *keyword):
        if len(keyword)==1:
            self.m_TempPoint = keyword[0]
        elif len(keyword)==2:
            self.m_TempPoint.x = keyword[0]
            self.m_TempPoint.y = keyword[1]
    def MakePermanent(self):
        self.m_PreviousPoint = self.m_Point
        self.m_Point = self.m_TempPoint
        self.m_RotationAngle = self.m_TempRotationAngle
        self.m_OriginalDrawCircleRadius = self.m_DrawCircleRadius
        self.m_OriginalSlideRadius = self.m_SlideRadius
    def __str__(self):return "<Point center={v.m_Point}".format(v = self)    
    def SetRPM(self, Value): self.m_RPM = Value
    def SetTempFixed(self, bSet): self.m_bTempFixed = bSet
    def SetRotationAngle(self, Value): self.m_TempRotationAngle = Value
    def IncrementRotationAngle(self, Change):
        Angle = self.GetRotationAngle()
        Angle += Change
        self.SetRotationAngle( Angle )
    def RotateAround(self, Point, Angle):
        self.SetTempFixed(True)
        self.m_TempPoint.RotateAround( Point, Angle)
        
    def SetAsDrawing(self, bset):self.m_bDrawingConnector = bSet
    def SetAsInput(self, bset):self.m_bInput = bSet
    def SetAsAnchor(self, bset):self.m_bAnchor = bSet
    def SetAlwaysManual(self, bset):self.m_bAlwaysManual = bSet
    def Select(self, bSelected): self.m_bSelected = bSelected
    def GetLinkList(self): return self.m_Links
    def AddMotionPoint(self):
        if not self.m_bDrawingConnector:
            return
        self.m_DrawingPointCounter +=1
        if self.m_DrawingPointCounter <3:
            return
        self.m_DrawingPointCounter = 0
        Point = self.GetPoint()
        if self.m_PointCount < MAX_DRAWING_POINTS:
            if self.m_PointCount > 0 and self.m_DrawingPoints[self.m_PointCount] == Point:
                return
            self.m_DrawingPoints[self.m_PointCount] = Point
            self.m_PointCount +=1
        else:
            PreviousPoint= MAX_DRAWING_POINTS - 1 if self.m_StartPoint == 0 else self.m_StartPoint - 1
            if self.m_DrawingPoints[PreviousPoint] == Point:
                return
            self.m_DrawingPoints[self.m_StartPoint] = Point
            self.m_StartPoint +=1
            if self.m_StartPoint == MAX_DRAWING_POINTS:
                self.m_StartPoint = 0
    def SetIntermediateDrawCircleRadius(self, Radius): self.m_DrawCircleRadius = abs( Radius )
    def SetDrawCircleRadius(self):return self.m_DrawCircleRadius
    def GetOriginalDrawCircleRadius(self):return self.m_OriginalDrawCircleRadius
    def SetIntermediateSlideRadius(self, Radius):self.m_SlideRadius = Radius
    def SetSlideRadius(self, Radius):
        self.m_SlideRadius = Radius
        self. m_OriginalSlideRadius = Radius
    def GetSlideRadius(self):
        if self.m_SlideRadius == 0:
            return 0
        sign = copysign( 1, self.m_SlideRadius )
        pLimit1 = CConnector()
        pLimit2 = CConnector()
        if not self.GetSlideLimits(pLimit1, pLimit2):
            return 0
        return sign*max(abs( self.m_SlideRadius ), ( self.Distance( pLimit1.GetPoint(), pLimit2.GetPoint())/2) + 0.0009)
        
    def GetOriginalSlideRadius(self):
        if( self.m_OriginalSlideRadius == 0 ):
            return 0
        sign = copysign( 1, self.m_SlideRadius )
        pLimit1 = CConnector()
        pLimit2 = CConnector()
        if not self.GetSlideLimits(pLimit1, pLimit2):
            return 0
        return sign * max(abs( self.m_OriginalSlideRadius), self.Distance( pLimit1.GetOriginalPoint(), pLimit2.GetOriginalPoint() ) / 2)
    def GetSliderArc(self, TheArc, bGetOriginal):
        if self.GetSlideRadius() ==0:
            return False
        pLimit1 = CConnector()
        pLimit2 = CConnector()
        if not self.GetSlideLimits(pLimit1, pLimit2):
            return False
        Point1 =  pLimit1.GetOriginalPoint() if bGetOriginal else pLimit1.GetPoint()
        Point2 =  pLimit2.GetOriginalPoint() if bGetOriginal else pLimit2.GetPoint()
        Line = CFLine( Point1, Point2 )
        Perpendicular = CFLine()
        aLength = Line.GetDistance() / 2
        Radius = self.GetSlideRadius()
        bLength = sqrt( ( Radius * Radius ) - ( aLength * aLength ) )
        Line.SetDistance( aLength )
        Line.PerpendicularLine( Perpendicular, bLength if Radius > 0 else -bLength)
        if( Radius > 0 ):
            TheArc.SetArc( Perpendicular.GetEnd(), Radius, Point1, Point2 )
        else:
            TheArc.SetArc( Perpendicular.GetEnd(), Radius, Point2, Point1 )
        return True
        
    def UpdateControlKnob(self, *keyword):
        if len(keyword)==0:
            pControlKnob = self.GetControlKnob()
            if self.m_DrawCircleRadius == 0.0 or pControlKnob == 0 :
                return
            Point = pControlKnob.GetPoint()
            Center = self.GetPoint()
            if Point == Center:
                Point += CFPoint( 10, 10 )
            Line = CFLine( self.GetPoint(), Point )
            Line.SetDistance( self.m_DrawCircleRadius )
            pControlKnob.SetPoint( Line.GetEnd())
        elif len(keyword)==1:
            Point = keyword[0]
            pControlKnob = self.GetControlKnob()
            if self.m_DrawCircleRadius == 0.0 or pControlKnob == 0:
                return
            Point = pControlKnob.SetPoint( Point )
            self.m_DrawCircleRadius = Distance( self.GetPoint(), Point )
            if (self.m_DrawCircleRadius <= 0.0):
                self.m_DrawCircleRadius = 0.001
            self.m_OriginalDrawCircleRadius = self.m_DrawCircleRadius
            
    def IsLinkSelected(self):
        Position = self.m_Links.GetHeadPosition()
        for Counter in range(Position != None):
            pLink = self.m_Links.GetNext( Position )
            if( pLink == 0 ):
                continue
            if( pLink.IsSelected() ):
                return True
        return False
    def IsAnchor(self):return self.m_bAnchor
    def IsInput(self):return self.IsInput
    def IsSlider(self):return self.m_pSlideLimits[0] != 0 and self.m_pSlideLimits[1] != 0
    def IsDrawing(self): return self.m_bDrawingConnector
    def IsTempFixed(self):return self.m_bTempFixed
    def IsFixed(self):return self.m_bTempFixed | self.m_bAnchor | self.m_bInput
    def IsAlwaysManual(self):return self.m_bAlwaysManual
    def GetSelectedLinkCount(self):
        Count = 0
        Position = self.m_Links.GetHeadPosition()
        for Counter in range(Position != None):
            pLink = self.m_Links.GetNext( Position )
            if( pLink == 0 or not pLink.IsSelected() ):
                continue
            Count =Count+1
            
        return Count
    def GetSlideLimits(self, *keyword):
        if type(keyword[0])==CConnector:
            keyword[0] = self.m_pSlideLimits[0]
            keyword[1] = self.m_pSlideLimits[1]
            return self.IsSlider()
        elif type(keyword[0])==CFPoint:
            if self.m_pSlideLimits[0] != 0:
                keyword[0] = self.m_pSlideLimits[0].GetPoint()
            if(  self.m_pSlideLimits[1] != 0 ):
                keyword[1] = self.m_pSlideLimits[1].GetPoint()
            return self.IsSlider() and self.m_pSlideLimits[0] != 0
    def GetLink(self, Index):
        Position = self.m_Links.GetHeadPosition()
        Counter=0
        for Counter in range(Position != None):
            pLink = self.m_Links.GetNext( Position )
            if( Counter == Index ):
                return pLink
        return 0
    def GetPoint(self):return self.m_Point
    def GetPreviousPoint(self): return self.m_PreviousPoint
    def GetTempPoint(self): return self.m_OriginalPoint if self.IsAnchor() else self.m_TempPoint
    def GetOriginalPoint(self):return self.m_OriginalPoint
    def GetRPM(self):return self.m_RPM
    def GetIdentifierString(self, bDebugging):
        pass
    def GetLinkCount(self): return self.m_Links.GetCount()
    def PointOnConnector(self, Point, TestDistance):
        Distance = self.m_Point.DistanceToPoint( Point )
        return Distance <= TestDistance
    def GetRotationAngle(self):return self.m_RotationAngle
    def GetTempRotationAngle(self):return self.m_TempRotationAngle
    def MakeAnglePermenant(self):self.m_RotationAngle = self.m_TempRotationAngle
    def GetArea(self, Rect):
        Point = self.GetPoint()
        Rect.left = Point.x - self.m_DrawCircleRadius
        Rect.top = Point.y + self.m_DrawCircleRadius
        Rect.right = Point.x + self.m_DrawCircleRadius
        Rect.bottom = Point.y - self.m_DrawCircleRadius
    def GetAdjustArea(self, Rect):
        Point = self.GetPoint()
        Rect.left = Point.x - self.m_DrawCircleRadius
        Rect.top = Point.y + self.m_DrawCircleRadius
        Rect.right = Point.x + self.m_DrawCircleRadius
        Rect.bottom = Point.y - self.m_DrawCircleRadius
    def GetMotionPath(self, StartPoint, PointCount, MaxPoint):
        if self.m_PointCount < 2:
            return 0
        StartPoint = self.m_StartPoint
        PointCount = self.m_PointCount;
        MaxPoint = MAX_DRAWING_POINTS - 1;
        return self.m_DrawingPoints;
    def HasLink(self, pLink):
        Position = self.m_Links.GetHeadPosition()
        while( Position != 0 ):
            RemovePosition = Position
            pCheckLink = self.m_Links.GetNext( Position )
            if( pCheckLink != 0 and pLink == pCheckLink ):
                return True
        return False
    def IsAlone(self):
        if self.m_Links.GetCount() > 1:
            return False
        Position = self.m_Links.GetHeadPosition()
        if( Position != 0 ):
            pCheckLink = self.m_Links.GetNext( Position )
            if( pCheckLink.GetConnectorCount() == 1 ):
                return True
        return False
    def SlideBetween(self, pConnector1 = 0, pConnector2 = 0):
        if pConnector2 == 0:
            pConnector1 == 0
        bSet = pConnector1 != 0
        pLink = CLink(0)
        if( bSet ):
            pLink = pConnector1.GetSharingLink( pConnector2 )
            if( pLink == 0 ):
                return
        elif self.m_pSlideLimits[0] != 0 and self.m_pSlideLimits[1] != 0:
            pLink = self.m_pSlideLimits[0].GetSharingLink( self.m_pSlideLimits[1] )
        if pLink != 0:
            pLink.SlideBetween( self, pConnector1, pConnector2 )
        self.m_pSlideLimits[0] = pConnector1;
        self.m_pSlideLimits[1] = pConnector2
        
    def GetSharingLink(self, pOtherConnector):
        Position = self.m_Links.GetHeadPosition()
        Counter = 0
        for Counter in range(Position != None):
            pLink = self.m_Links.GetNext( Position )
            if( pLink == 0 ):
                continue
            if( pOtherConnector.HasLink( pLink ) ):
                return pLink
        return 0
        
    def IsSharingLink(self,pOtherConnector):
        if( self.GetSharingLink( pOtherConnector ) != 0 ):
            return True
        return self.IsAnchor() and pOtherConnector.IsAnchor()
        
    def AddLink(self,pLink):
        if self.m_Links.Find( pLink ) == 0:
            self.m_Links.AddTail( pLink )
    def RemoveAllLinks(self): self.RemoveLink( 0 )
    def RemoveLink(self, pLink):
        Position = self.m_Links.GetHeadPosition()
        while( Position != 0 ):
            RemovePosition = Position
            pCheckLink = self.m_Links.GetNext( Position )
            if( pCheckLink != 0 and ( pLink == 0 or pCheckLink == pLink ) ):
                self.m_Links.RemoveAt( RemovePosition )
                pCheckLink.SetActuator( pCheckLink.IsActuator() and pCheckLink.GetConnectorCount() == 2 )

if __name__ == '__main__':
    a = CConnector()
    a.SetPoint(10, 5)
    a.SetPoint(5,10)
    a.MovePoint(5,20)
    print(a.GetTempPoint())
    #b = CFPoint(20, 5) 
