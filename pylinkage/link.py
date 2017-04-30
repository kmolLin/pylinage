#link.py
DBL_MAX = 1.7976931348623158e+308 ## max value
from Element import CElement
from Connector import  *
from geometry import CFPoint
class LinkList(list):
    
    def Remove(self, pLink):
        Position = self[0]
        while( Position != 0 ):
            RemovePosition = Position
            pCheckLink =  self[Position+1]
            if( pCheckLink != 0 and ( pLink == 0 or pCheckLink == pLink  ) ):
                self.pop( RemovePosition )
                return True
        return True

    def Contains(self, pLink): return pLink in self
    def __getitem__(self, k):
        if len(self)==0:
            print('error')
        else:
            return self[k]
    def __str__(self): return "<list x={v[0]}>".format(v=self)

class CGearConnection():
    ##enum ConnectionType { GEARS, CHAIN }
    GEARS = 0
    CHAIN = 1
    def CGearConnection(self):
        self.m_pGear1 = 0;
        self.m_pGear2 = 0;
        self.m_pDriveGear = 0;
        self.m_Gear1Size = 0.0;
        self.m_Gear2Size = 0.0;
        self.m_ConnectionType = self.GEARS;
        self.m_bUseSizeAsRadius = False;
    def Ratio(self):return self.m_Gear2Size / self.m_Gear1Size

class CLinkTriangleConnection():
    pOriginalConnector = CConnector()
    pReplacementConnector =CConnector()

class CLink(CElement):
    def __init__(self,*keyword):
        self.m_Connectors = ConnectorList()
        if len(keyword)==0:
            self.m_Identifier = 0
            self.m_MoveCount = 0
            self.m_bSelected = False
            self.m_bTempFixed = False
            self.m_bActuator = False
            self.m_bAlwaysManual = False
            self.m_ActuatorStroke = 0
            self.m_ActuatorCPM = 0
            self.m_LineSize = 1
            self.m_bSolid = 0
            self.m_ActuatorExtension = 0
            self.m_TempActuatorExtension = 0
            self.m_pHull = 0
            self.m_HullCount = 0
            self.m_bGear = False
            self.m_RotationAngle = 0.0
            self.m_TempRotationAngle = 0.0
            #self.m_Color = RGB( 200, 200, 200 )
            self.m_bLocked = False
            self.m_ActuatorStartOffset = 0;
        elif len(keyword) ==1:
            ExistingLink = keyword[1]
            self.m_bSelected = False
            self.m_bTempFixed = ExistingLink.m_bTempFixed
            self.m_Identifier = ExistingLink.m_Identifier
            self.m_MoveCount = ExistingLink.m_MoveCount
            self.m_LineSize = ExistingLink.m_LineSize
            self.m_bSolid = ExistingLink.m_bSolid
            self.m_ActuatorCPM = ExistingLink.m_ActuatorCPM
            self.m_ActuatorStroke = ExistingLink.m_ActuatorStroke
            self.m_ActuatorExtension = 0
            self.m_TempActuatorExtension = 0
            self.m_bAlwaysManual = ExistingLink.m_bAlwaysManual
            self.m_RotationAngle = ExistingLink.m_RotationAngle
            self.m_bGear = ExistingLink.m_bGear
            self.m_bLocked = ExistingLink.m_bLocked
            self.m_bMeasurementElement = ExistingLink.m_bMeasurementElement
            self.m_bNoRotateWithAnchor = ExistingLink.m_bNoRotateWithAnchor
            self.m_Layers = ExistingLink.m_Layers
            self.m_Color = ExistingLink.m_Color
            self.m_bActuator = ExistingLink.m_bActuator
            self.m_bNoRotateWithAnchor = ExistingLink.m_bNoRotateWithAnchor
            self.m_pHull = 0
            self.m_HullCount = 0

            Position = ExistingLink.m_Connectors.GetHeadPosition()
            while( Position != 0 ):
                pConnector = ExistingLink.m_Connectors.GetNext( Position )
                if( pConnector == 0 ):
                    continue
                self.m_Connectors.append( pConnector )
    def IsLink(self):return True
    def IsConnector(self):return False
    def GetLocation(self):return CFPoint() if len(self.m_Connectors) else CConnector(self.m_Connectors[0]).GetPoint()
    def GetIdentifierString(self,bDebugging):
        if( bDebugging ):
            print(self.GetIdentifier())
    def GetConnectorList(self):return self.m_Connectors
    def AddConnector(self,pConnector):
        if( self.m_Connectors.Find( pConnector ) != 0 ):
            return
        self.m_Connectors.append( pConnector )
    def SelectAllConnectors(self,bSelected):
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector != 0 ):
                pConnector.Select( bSelected )
        self.Select( bSelected )

    def SetTempFixed(self,bSet): self.m_bTempFixed = bSet
    def SetRotationAngle(self,Value):
        self.m_TempRotationAngle = Value 
        self.m_MoveCount +=1
    def GetRotationAngle(self):return self.m_RotationAngle
    def GetTempRotationAngle(self):return self.m_TempRotationAngle
    def IsGearAnchored(self):
        return self.IsGear() and self.GetFastenedTo() != 0 and self.GetFastenedTo().GetConnector() != 0 and self.GetFastenedTo().GetConnector().IsAnchor()
    def FixAllConnectors(self):pass
    def Reset(self):
        self.m_ActuatorExtension = 0
        self.m_TempActuatorExtension = 0
        self.m_RotationAngle = 0.0
        self.m_TempRotationAngle = 0.0
        self.SetPositionValid( True )
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector != 0 ):
                pConnector.Reset( False )
    def IsTempFixed(self):return self.m_bTempFixed
    def IsFixed(self):return self.m_bTempFixed
    def GetLength(self):
        if( self.m_Connectors.GetCount() != 2 ):
            return 0
        pConnector1 = self.GetConnector( 0 )
        pConnector2 = self.GetConnector( 1 )
        return self.Distance( pConnector1.GetOriginalPoint(), pConnector2.GetOriginalPoint())
    ####100行
    def IsAllSelected(self):
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pCheckConnector = self.m_Connectors.GetNext( Position )
            if( pCheckConnector != 0 and not pCheckConnector.IsSelected() ):
                return False
        return True
    def IsAnySelected(self):
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pCheckConnector = self.m_Connectors.GetNext( Position )
            if( pCheckConnector != 0 and pCheckConnector.IsSelected()):
                return True
        return False
    def IsConnected(self, pConnector):
        return self.m_Connectors.Find( pConnector ) != 0
    def GetSelectedConnectorCount(self):
        Count = 0
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pCheckConnector = self.m_Connectors.GetNext( Position )
            if( pCheckConnector != 0 and pCheckConnector.IsSelected()):
                Count += 1
        return Count
    def GetArea(self, GearConnectionList, GearConnections, Rect):
        AreaRect = CFRect( DBL_MAX, -DBL_MAX, -DBL_MAX, DBL_MAX )
        ConnectorCount = 0
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector == 0 ):
                continue
            TempRect = CFRect()
            pConnector.GetArea( TempRect )
            AreaRect.left = min( AreaRect.left, TempRect.left )
            AreaRect.right = max( AreaRect.right, TempRect.right )
            AreaRect.top = max( AreaRect.top, TempRect.top )
            AreaRect.bottom = min( AreaRect.bottom, TempRect.bottom )
        if( self.m_bGear ):
            pConnector = self.GetConnector( 0 )
            Radius = self.GetLargestGearRadius( GearConnections, 0 )
            AreaRect.left = min( AreaRect.left, pConnector.GetPoint().x - Radius )
            AreaRect.right = max( AreaRect.right, pConnector.GetPoint().x + Radius )
            AreaRect.top = max( AreaRect.top, pConnector.GetPoint().y + Radius )
            AreaRect.bottom = min( AreaRect.bottom, pConnector.GetPoint().y - Radius)
        Rect = AreaRect
    def GetConnectorCount(self):return self.m_Connectors.GetCount()
    def GetAnchorCount(self):
        Count = 0
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pCheckConnector = self.m_Connectors.GetNext( Position )
            if( pCheckConnector != 0 and pCheckConnector.IsAnchor() ):
                Count +=1
        return Count
    def CanOnlySlide(self, pLimit1 = 0, pLimit2 = 0,pSlider1 = 0, pSlider2 = 0, pbSlidersOnLink = 0 ):
        pConnectorList = ConnectorList(self.m_ConnectedSliders)
        Try = 0
        for Try in range(2):
            pConnectorList = self.m_Connectors
            Position = pConnectorList.GetHeadPosition()
            while( Position != 0 ):
                pCheckSlider1 = pConnectorList.GetNext( Position )
                if( pCheckSlider1 == 0 or not pCheckSlider1.IsSlider()):
                    continue
                if Try == 0:
                    if( not pCheckSlider1.IsFixed() ):
                        continue
                pLimit1_1 = CConnector(0)
                pLimit1_2 = CConnector(0)
                if( not pCheckSlider1.GetSlideLimits( pLimit1_1, pLimit1_2 )):
                    continue
                if Try ==1:
                    if( not pLimit1_1.IsFixed() or not pLimit1_2.IsFixed() ):
                        continue
                Position2 = pConnectorList.GetHeadPosition()
                while( Position2 != 0 ):
                    pCheckSlider2 = pConnectorList.GetNext( Position2 )
                    if( pCheckSlider2 == 0 or not pCheckSlider1.IsSlider() or pCheckSlider2 == pCheckSlider1 ):
                        continue
                    if( Try == 0 ):
                        if( not pCheckSlider2.IsFixed()):
                            continue
                    pLimit2_1 = CConnector(0)
                    pLimit2_2 = CConnector(0)
                    if(not pCheckSlider2.GetSlideLimits( pLimit2_1, pLimit2_2 )):
                        continue
                    if( Try == 1 ):
                        if(not pLimit2_1.IsFixed() or not pLimit2_2.IsFixed()):
                            continue
                    if( ( pLimit1_1 == pLimit2_1 and pLimit1_2 == pLimit2_2) or
                    ( pLimit1_1 == pLimit2_2 and pLimit1_2 == pLimit2_1 ) ):
                        if( pLimit1 != 0 ):pLimit1 = pLimit1_1
                        if( pLimit2 != 0 ):pLimit2 = pLimit1_2
                        Distance1 = self.Distance( pCheckSlider1.GetOriginalPoint(), pLimit1_1.GetOriginalPoint())
                        Distance2 = self.Distance( pCheckSlider1.GetOriginalPoint(), pLimit1_2.GetOriginalPoint())
                        if( Distance1 < Distance2 ):
                            if( pSlider1 != 0 ):
                                pSlider1 = pCheckSlider1
                            if( pSlider2 != 0 ):
                                pSlider2 = pCheckSlider2
                        else:
                            if( pSlider1 != 0 ):pSlider1 = pCheckSlider2
                            if( pSlider2 != 0 ):pSlider2 = pCheckSlider1
                        if( pbSlidersOnLink != 0 ):pbSlidersOnLink = Try == 1
                        return True
        return False
        
    def ComputeHull(self, Count = 0, bUseOriginalPoints = False):
        if( self.m_pHull != 0 ): self.m_pHull=[]
        self.m_pHull = self.GetHull(self.m_Connectors, self.m_HullCount, bUseOriginalPoints)
        if( self.m_pHull == 0 ):self.m_HullCount = 0
        if( Count != 0 ):Count = 0 if self.m_HullCount <0 else self.m_HullCount
        return self.m_pHull
    def GetHull(self, Count, bUseOriginalPoints):
        self.ComputeHull( 0, bUseOriginalPoints )
        Count = self.m_HullCount
        return self.m_pHull
        
    def MakePermanent(self):
        self.m_ActuatorExtension = self.m_TempActuatorExtension
        self.m_RotationAngle = self.m_TempRotationAngle
    def GetTempActuatorExtension(self):return self.m_TempActuatorExtension
    def InitializeForMove(self):
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector == 0 ):
                continue
            pConnector.MovePoint( pConnector.GetPoint())
            pConnector.SetPositionValid(True)
    def ResetMoveCount(self):self.m_MoveCount = 0
    def GetMoveCount(self):return self.m_MoveCount
    def IncrementMoveCount(self, Increment = +1):self.m_MoveCount += Increment
    def GetLineSize(self):return self.m_LineSize
    def SetLineSize(self, Size):self.m_LineSize = 0 if Size <= 0 else 1
    def IsSolid(self):return self.m_bSolid
    def SetSolid(self, bSolid):self.m_bSolid = bSolid
    def IsLocked(self):return self.m_bLocked
    def SetLocked(self, bLocked):self.m_bLocked = bLocked
    def GetStartOffset(self):return self.IsActuator() if self.m_ActuatorStartOffset else 0
    def IsGear(self):return self.m_bGear
    def SetGear(self, bSet):self.m_bGear = bSet
    def GetGearConnector(self):return self.GetConnector( 0 )if self.m_bGear else 0
    def IsActuator(self):return self.m_bActuator
    def SetActuator(self, bActuator):
        if( self.GetConnectorCount() != 2 and self.GetConnectorCount() != 0 ):
            self.m_bActuator = False
            return
        bNewActuator = bActuator and not self.m_bActuator
        self.m_bActuator = bActuator
        if( bNewActuator ):
            Position = self.m_Connectors.GetHeadPosition()
            if( Position == 0 ):
                return
            pConnector1 = self.m_Connectors.GetNext( Position )
            if( Position == 0 ):
                return
            pConnector2 = self.m_Connectors.GetNext( Position )
            pControlKnob = self.GetControlKnob()
            if( pControlKnob != 0 ):
                pControlKnob.SetParent( self )
                pControlKnob.SetSlideLimits( pConnector1, pConnector2 )
                pControlKnob.SetShowOnParentSelect( True )
            Line = CFLine( pConnector1.GetPoint(), pConnector2.GetPoint())
            self.m_ActuatorCPM = 15
            self.SetStroke( Line.GetDistance() / 2 )
    def SetAlwaysManual(self, bSet):self.m_bAlwaysManual = bSet
    def IsAlwaysManual(self):return self.m_bAlwaysManual
    def GetStroke(self):return self.m_ActuatorStroke
    def GetStrokePoint(self, Point):
        Point.SetPoint( 0, 0 )
        if( not self.m_bActuator or self.GetConnectorCount() != 2 ):
            return False
        Position = self.m_Connectors.GetHeadPosition()
        if( Position == 0 ):
            return False
        pConnector1 = self.m_Connectors.GetNext( Position )
        if( Position == 0 ):
            return False
        pConnector2 = self.m_Connectors.GetNext( Position )
        Line = CFLine(pConnector1.GetPoint(), pConnector2.GetPoint())
        Distance = Line.GetDistance()
        if( self.m_ActuatorStroke < Distance ):
            Distance = self.m_ActuatorStroke
        Line.SetDistance( self.m_ActuatorStroke )
        Point = Line.GetEnd()
        return True
    def SetStroke(self, Stroke):
        self.m_ActuatorStroke = Stroke
        self.m_ActuatorExtension = 0
        self.m_TempActuatorExtension = 0
        self.UpdateControlKnob()
    def GetCPM(self):return self.m_ActuatorCPM
    def SetCPM(self, CPM):self.m_ActuatorCPM = CPM
    def IncrementExtension(self, Increment):
        self.SetExtension( self.m_TempActuatorExtension + Increment )
    def SetExtension(self, Value):
        self.m_TempActuatorExtension = Value
        while( self.m_TempActuatorExtension > self.m_ActuatorStroke * 2 ):
            self.m_TempActuatorExtension -= self.m_ActuatorStroke * 2
        while( self.m_TempActuatorExtension < 0 ):
            self.m_TempActuatorExtension += self.m_ActuatorStroke * 2
    def GetExtendedDistance(self):
        UseDistance = abs( self.m_TempActuatorExtension )
        if( UseDistance > self.m_ActuatorStroke ):
            UseDistance = self.m_ActuatorStroke - ( UseDistance - self.m_ActuatorStroke )
        else:
            UseDistance = self.m_TempActuatorExtension
        return UseDistance*(1 if self.m_ActuatorCPM >= 0 else -1)
    def UpdateControlKnob(self, *keyword):
        if len(keyword) ==1:
            pControlKnob = self.GetControlKnob()
            if( not self.IsActuator() or pControlKnob == 0 ):
                return
            keyword[0] = pControlKnob.SetPoint( keyword[0] )
            Count = self.GetConnectorCount()
            if( Count != 2 ):
                return
            Position = self.m_Connectors.FindIndex( 0 )
            if( Position == 0 ):
                return
            pConnector1 = self.m_Connectors.GetAt( Position )
            if( pConnector1 == 0 ):
                return
            Line = CFLine(pConnector1.GetPoint(), self.m_ControlKnob.GetPoint())
            self.SetStroke( Line.GetDistance())
        if len(keyword) ==0:
            if( not self.IsActuator() ):
                return
            Point = CFPoint()
            self.GetStrokePoint( Point )
            self.m_ControlKnob.SetPoint( Point )
        
    def GetConnectedSliderCount(self):self.m_ConnectedSliders.GetCount()
    def GetConnectedSlider(self, Index):
        Counter = 0
        Position = self.m_ConnectedSliders.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_ConnectedSliders.GetNext( Position )
            if( pConnector == 0 ):
                continue
            if  Counter == Index:
                return pConnector
            Counter = Counter+1
        return 0
    def GetLinkLength(self, pFromConnector, pToConnector):return self.GetActuatedConnectorDistance( pFromConnector, pToConnector )
    def GetActuatedConnectorDistance(self, pConnector1, pConnector2):
        pLink = CLink(pConnector1.GetSharingLink( pConnector2 ))
        if( not self.m_bActuator or pLink == 0 ):
            return self.Distance( pConnector1.GetOriginalPoint(), pConnector2.GetOriginalPoint() )
        return self.Distance( pConnector1.GetOriginalPoint(), pConnector2.GetOriginalPoint() ) + self.GetExtendedDistance()
    def RemoveConnector(self, pConnector):
        if( pConnector == 0 ):
            self.m_Connectors.RemoveAll()
            self.m_ConnectedSliders.RemoveAll()
        else:
            self.m_Connectors.Remove( pConnector )
            self.m_ConnectedSliders.Remove( pConnector )
    def RemoveAllConnectors(self):self.RemoveConnector( 0 )
    def SlideBetween(self, pSlider = 0, pConnector1 = 0, pConnector2 = 0):
        if( pConnector1 == 0 or pConnector2 == 0 ):
            self.m_ConnectedSliders.Remove( pSlider )
        else:
            if( self.m_ConnectedSliders.Find( pSlider ) != 0 ):
                return
            self.m_ConnectedSliders.append( pSlider )
        
    def GetFixedConnectorCount(self):
        Count = 0
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector == 0 ):
                continue
            if( pConnector.IsAnchor() or pConnector.IsTempFixed()):
                Count = Count+1
        return Count
    def GetFixedConnector(self):
        Count = 0
        pFixedConnector = 0
        Position = self.m_Connectors.GetHeadPosition()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector == 0 ):
                continue
            if( pConnector.IsAnchor() or pConnector.IsTempFixed() ):
                pFixedConnector = pConnector
                Count = Count+1
        return pFixedConnector if Count == 1 else 0 
    def RotateAround(self):
        pass ##???
    def FixAll(self):
        if( self.IsGear() ):
            self.SetRotationAngle(0)
            self.SetTempFixed( True )
            return True
        if( self.GetFixedConnectorCount() < 2 ):
            return False
        pPreviousFixed = CConnector(0)
        pFixed1 = CConnector(0)
        pFixed2 = CConnector(0)
        Position = self.m_Connectors.GetHeadPosition()
        pBaseConnector = self.GetFixedConnector()
        while( Position != 0 ):
            pConnector = self.m_Connectors.GetNext( Position )
            if( pConnector == 0 ):
                continue
            if( pConnector.IsFixed() ):
                pFixed1 = pConnector
                if (pPreviousFixed != 0):
                    d1 = self.Distance( pFixed1.GetOriginalPoint(), pPreviousFixed.GetOriginalPoint() )
                    d2 = self.Distance( pFixed1.GetPoint(), pPreviousFixed.GetPoint() )
                    Difference = abs( d2 - d1 )
                    if( Difference > ( d1 / 1000.0 ) ):
                        return False
                    pFixed2 = pPreviousFixed
                    pPreviousFixed = pConnector
        pFixed1.SetRotationAngle( self.GetAngle( pFixed1.GetTempPoint(), pFixed2.GetTempPoint(), pFixed1.GetOriginalPoint(), pFixed2.GetOriginalPoint() ) )
        if( not self.RotateAround( pFixed1 ) ):
            return False
        return True
    def GetCommonConnector(self, pLink1, pLink2):
        if( pLink1 == 0 or pLink2 == 0):
            return 0
        Position1 = pLink1.GetConnectorList().GetHeadPosition()
        while( Position1 != 0 ):
            pConnector1 = pLink1.GetConnectorList().GetNext( Position1 )
            if( pConnector1 == 0 ):
                continue
            Position2 = pLink2.GetConnectorList().GetHeadPosition()
            while( Position2 != 0 ):
                pConnector2 = pLink2.GetConnectorList().GetNext( Position2 )
                if( pConnector1 == pConnector2 ):
                    return pConnector1
        return 0
    def GetControlKnob(self):
        self.UpdateControlKnob()
        return self.m_ControlKnob if self.IsActuator() else 0
    
if __name__ =="__main__":
    a = LinkList()
    b = CLink()
    print(b.GetIdentifierString(10))
    a.append(b)
    print(b.GetConnectorList())
    #print(a)
