#Simulator
from linkageDoc import CLinkageDoc

class CSimulator():
    def __init__(self):
        self.m_pImplementation = self.CSimulatorImplementation()
        
class CSimulatorImplementation():
    def __init__(self):
        INTERMEDIATE_STEPS = 2
        self.m_bUseIncreasedMomentum = False
        self.m_bSimulationValid = False
        self.Reset()
        
    def Reset(self):
        self.m_SimulationStep = 0
        return True
        
    def IsSimulationValid(self):return self.m_bSimulationValid
    def Options(self, bUseIncreasedMomentum ):self.m_bUseIncreasedMomentum  = bUseIncreasedMomentum 
    def CommonDivisor(self, Values, Count):
        while():
            Counter =0
            for Counter in range(Count):
                if( Values[Counter] == 1 ):
                    return 1
            NonzeroValue = 0
            NonzeroCount = 0
            Counter =0
            for Counter in range(Count):
                if( Values[Counter] == 0 ):
                    continue
                NonzeroValue = Values[Counter]
                NonzeroCount=NonzeroCount+1
            if( NonzeroCount == 1 ):
                return NonzeroValue
            
                '''
                Find the lowest value and then change all of the other values
                to be the remainder of the value divided by the lowest value
                 '''
            LowestLocation = -1
            LowestValue = 999999999
            Counter=0
            for (Counter) in range(Count):
                if( Values[Counter] < LowestValue ):
                    LowestLocation = Counter
                    LowestValue = Values[Counter]
            
            Counter=0
            for (Counter) in range(Count):
                if( Counter == LowestLocation ):
                    continue
                Values[Counter] %= LowestValue
                
            '''The new values will get processed at the top of the loop. This
            * computation will continue until one of the conditions up there
            * is met and we return something. The loop does not have a maximum
            * loop count because the compuations are guanranteed to have an
            * effect, to the best of my knowledge.'''
            
    def GetSimulationSteps(self, pDoc):
        InputCount = 0
        Position = pDoc.GetConnectorList[0] ##need change
        Count = 0
        pLastInput = CConnector(0)
        while( Position != None ):
            pConnector = pDoc.GetConnectorList()[Position]
            if( pConnector == 0 ):
                continue
            if( pConnector.IsInput() ):
                InputCount+=1
        Position = pDoc.GetLinkList()[0]
        Index = 0
        while( Position != None ):
            pConnector = pDoc.GetConnectorList()[Position+1]
            if ( pConnector == 0 ):
                continue
            if( pConnector.IsInput() ):
                InputCount+=1
                
        Position = pDoc.GetLinkList()[0]
        while( Position != None ):
            pLink = pDoc.GetLinkList()[Position+1]
            if( pLink == 0 ):
                continue
            if( pLink.IsActuator() ):
                InputCount = InputCount+1
        if( InputCount == 0 ):
            return 1
        
        Values = [None for i in range(InputCount)]
        if( len(Values) == 0 ):
            return 0
        Position  = pDoc.GetConnectorList()[0]
        Index = 0
        while( Position != None ):
            pConnector = pDoc.GetConnectorList()[Position +1]
            if pConnector == 0:
                continue
            if( pConnector.IsInput() ):
                Values[Index] = abs(pConnector.GetRPM())+.9999
                Index +=1
        Position = pDoc.GetLinkList()[0]
        while( Position != None ):
            pLink = pDoc.GetLinkList()[Position]
            if( pLink == 0 ):
                continue
            if pLink.IsActuator():
                Values[Index] = abs(pLink.GetRPM())+.9999
                Index +=1
        
        if( InputCount == 1 ):
            return 1800 / Values[0]
        Divisor = self.CommonDivisor( Values, InputCount )
        return 1800 / Divisor
        
    def SimulateStep(self,pDoc, StepNumber, bAbsoluteStepNumber, pInputID, pInputPositions, InputCount, bNoMultiStep ):
        if( pDoc == 0 ):
            return False
        self.m_bSimulationValid = True
        pConnectors = pDoc.GetConnectorList()
        pLinks = pDoc.GetLinkList()
        if( pConnectors == 0 or pLinks == 0 ):
            return False
        if( pConnectors.GetCount() == 0 or pLinks.GetCount() == 0 ):
            return False
        StepsToMove = StepNumber
        if( bAbsoluteStepNumber ):
            StepsToMove = StepNumber - m_SimulationStep
        elif InputCount > 0 and not bNoMultiStep:
            StepsToMove = 150
        TickCount = self.GetTickCount()
        MAX_TIME_TO_SIMULATE = 250
        Direction = 1 if StepsToMove > 0 else -1
        bResult = True
        StartStep = self.m_SimulationStep
        IgnoreTime = False
        while( StepsToMove != 0 and ( self.GetTickCount() < TickCount + MAX_TIME_TO_SIMULATE or IgnoreTime ) ):
            self.m_SimulationStep += Direction
            StepsToMove -= Direction
            TotalManualControlDistance = 0
            Counter = 0
            IntermediateStep = INTERMEDIATE_STEPS - 1
            for IntermediateStep in range(IntermediateStep >= 0 and bResult, IntermediateStep-1):
                Position = pConnectors[0]
                while( Position != 0 ):
                    pConnector = pConnectors[Position+1]
                    if( pConnector == 0 ):
                        continue
                    pConnector.SetTempFixed(False)
                    if( not pConnector.IsInput() ):
                        continue
                    for Counter in range(Counter < InputCount and pInputID[Counter] != 10000+ pConnector.GetIdentifier()):
                        Counter+=1
                    if Counter == InputCount:
                        if not pConnector.IsAlwaysManual():
                            pConnector.SetRotationAngle(((self.m_SimulationStep*INTERMEDIATE_STEPS )-(IntermediateStep*Direction))*(-(pConnector.GetRPM() * 0.2 ) / INTERMEDIATE_STEPS ) )
                            pConnector.MakeAnglePermenant()
                    else:
                        DesiredAngle = 0
                        if( pInputPositions[Counter] != 0 ):
                            DesiredAngle = 360 - ( 360.0 * pInputPositions[Counter] )
                            Difference = DesiredAngle - pConnector.GetRotationAngle()
                            if( Difference > 180.0 ):
                                Difference -= 360.0
                            if( Difference > 2 ):
                                Difference = 2
                            elif( Difference < -2 ):
                                Difference = -2
                            Difference /= INTERMEDIATE_STEPS
                            if( Difference != 0 ):
                                pConnector.IncrementRotationAngle( Difference )
                                TotalManualControlDistance += Difference
                
            Position = pLinks.GetHeadPosition()
            while( Position != 0 ):
                pLink = pLinks[Position+1]
                if( pLink == 0  ):
                    continue
                pLink.SetTempFixed(False)
                pLink.InitializeForMove()
                if( not pLink.IsActuator() ):
                    continue
                    ###303
                pLink.SetTempFixed( False )
                pLink.InitializeForMove()
                if( not pLink.IsActuator() ):
                    continue
                Counter=0
                for Counter in range(Counter < InputCount and pInputID[Counter] != pLink.GetIdentifier()):
                    Counter +=1
                if Counter == InputCount:
                    if( not pLink.IsAlwaysManual() ):
                        Distance = pLink.GetStroke() * abs( pLink.GetCPM() ) / 900.0
                        pLink.SetExtension( ( ( self.m_SimulationStep * INTERMEDIATE_STEPS ) - ( IntermediateStep * Direction ) ) * ( Distance / INTERMEDIATE_STEPS ))
                else:
                    DesiredExtension = 0
                    if( pInputPositions[Counter] != 0 ):
                        DesiredExtension = pLink.GetStroke() * pInputPositions[Counter]
                    
                        
                    
                
    def ValidateMovement(self, pDoc):
        if( pDoc == 0 ):
            return False
        pConnectors = pDoc.GetConnectorList()
        pLinks = pDoc.GetLinkList()
        if( pConnectors == 0 or pLinks == 0 ):
            return False
        if( pConnectors.GetCount() == 0 or pLinks.GetCount() == 0 ):
            return False
        Position = pConnectors[0]
        while( Position != None ):
            pCheckConnector = pConnectors()[Position+1]
            if( pCheckConnector == 0 or not pCheckConnector.IsOnLayers( MECHANISMLAYERS ) ):
                continue
            if( not pCheckConnector.IsPositionValid() ):
                return False
        bResult = True
        Position = pConnectors[0]
        while( Position != None):
            pCheckConnector = pConnectors()[Position ]
            if( pCheckConnector == 0 or not pCheckConnector.IsOnLayers( MECHANISMLAYERS ) ):
               continue
            if(not pCheckConnector.IsFixed() ):
                pCheckConnector.SetPositionValid( False )
                bResult = False
                
        Position = pLinks[0]
        while( Position != 0 ):
            pLink = pLinks()[Position+1]
            if( pLink == 0 or not pLink.IsGear() ):
                continue
            if not pLink.IsTempFixed():
                pLink.SetPositionValid( False )
                bResult = False
                
        return bResult
        
    def CheckForMovement(self, pDoc, pLink):
        pGearConnections = pDoc.GetGearConnections()
        FixedCount = pLink.GetFixedConnectorCount()
        bResult = True
        if( FixedCount != pLink.GetConnectorCount() or not pLink.IsFixed() or pLink.IsGear() ):
            pFixed = pLink.GetFixedConnector()
            if( pFixed != 0 and pFixed.IsInput() ):
                if( not pLink.IsFixed() ):
                    if( pLink.IsGearAnchored() ):
                        bResult = pLink.FixAll()
                    else:
                        bResult = pLink.RotateAround( pFixed )
                        
                if( pLink.IsGear() ):
                    bResult = self.FindGearsToMatch( pLink, pGearConnections )
                    
            elif(pLink.IsGear()):
                if( pLink.IsGearAnchored() and not pLink.IsFixed() ):
                    bResult = pLink.FixAll()
                    bResult = self.FindGearsToMatch( pLink, pGearConnections )
                    
            elif  FixedCount <= 1:
                bResult = self.FindLinksToMatch( pLink )
                if( not bResult ):
                    bResult = self.FindSlideLinksToMatch( pLink, pDoc.GetLinkList() )
                if( not bResult ):
                    bResult = self.FindLinkTriangleMatch( pLink )
        else :
            bResult = self.FixAllIfPossible( pLink )
        return bResult
        
    def FixAllIfPossible(self, pLink):
        pFixedConnector = pLink.GetFixedConnector()
        if( pFixedConnector == 0 ):
            return False
        OriginalFixedPoint = pFixedConnector.GetOriginalPoint()
        FixedPoint = pFixedConnector.GetPoint()
        pConnectors = pLink.GetConnectorList()
        if( pConnectors == 0 ):
            return False
        Position = pConnectors[0]
        while( Position != 0 ):
            pConnector = pConnectors()[Position+1]
            if( pConnector == 0 or not pConnector.IsFixed() or pConnector == pFixedConnector ):
                continue
            OriginalDistance = self.Distance( OriginalFixedPoint, pConnector.GetOriginalPoint() )
            distance = self.Distance( FixedPoint, pConnector.GetPoint() )
            if( abs( OriginalDistance - distance ) > 0.0001 ):
                return False
        return pLink.FixAll()
    
    def MoveSimulation(self, pDoc):
        if( pDoc == 0 ):
            return False
        pConnectors = pDoc.GetConnectorList()
        pLinks = pDoc.GetLinkList()
        if( pConnectors == 0 or pLinks == 0 ):
            return False
        if( pConnectors.GetCount() == 0 or pLinks.GetCount() == 0 ):
            return False
        while():
            MoveCount = 0
            Position = pLinks[0]
            while( Position != 0 ):
                pLink = pLinks()[Position+1]
                if( pLink == 0 or not pLink.IsOnLayers( MECHANISMLAYERS)  ):
                    continue
                pLink.ResetMoveCount()
                self.CheckForMovement( pDoc, pLink )
                MoveCount += pLink.GetMoveCount()
            if( MoveCount == 0 ):
                break
        if( not ValidateMovement( pDoc ) ):
            Position = pConnectors[0]
            while( Position != 0 ):
                pConnector = pConnectors()[Position+1]
                if( pConnector == 0 ):
                    continue
                pConnector.AddMotionPoint()
            self.m_bSimulationValid = False
            return False
        Position = pConnectors[0]
        while( Position != 0 ):
            pConnector = pConnectors()[Position+1]
            if( pConnector == 0 ):
                continue
            pConnector.AddMotionPoint()
            pConnector.MakePermanent()
        Position = pLinks[0]
        while( Position != 0 ):
            pLink = pLinks()[Position+1]
            if( pLink == 0 ):
                continue
            pLink.MakePermanent()
            pLink.UpdateControlKnob()
        return True
        
    def JoinToSlideLinkSpecial(self, pLink, pFixedConnector, pCommonConnector, pOtherLink):
        '''
        /*
        * Rotate the "this" Link and slide the other link so that they are still
        * connected. The "this" Link has only one connection that is in a new
        * temp location, pFixedConnector, and the other Link needs to have two
        * fixed sliding connectors that it must slide through.
        *
        * The "this" Link will not have proper temp locations for all
        * connectors yet, only the fixed one. It is in an odd screwed up state
        * at the moment but will be fixed shortly.
        *
        * SPECIAL CASE: If this link IS pOtherLink link then we are only trying
        * to slide this link to a new position based on slider pCommonConnector
        * ( which is a slider but not one of the sliders that we are sliding ON).
        * The common connector has limits that are fixed and we can move this
        * link to a new position without changing any other link.
        *
        * This code is for the special case where the other link slides on a
        * curved slider path. The sliders must have the exact same slide radius
        * for this to work properly.
        */

        '''
        if( pCommonConnector == 0 ):
            return False
        bOtherLinkOnly =  ( pLink == pOtherLink and pFixedConnector == 0 )
        pLimit1 = 0
        pLimit2 = 0
        pSlider1 = 0
        pSlider2 = 0
        pActualSlider1 = 0
        pActualSlider2 = 0
        
        if( not pOtherLink.CanOnlySlide( pLimit1, pLimit2, pSlider1, pSlider2, bOtherLinkHasSliders ) ):
            return False
        pActualSlider1 = pSlider1
        pActualSlider2 = pSlider2
        if( pSlider1.GetSlideRadius() != pSlider2.GetSlideRadius() ):
            return False
        if( pCommonConnector == pSlider1 or pCommonConnector == pSlider2 ):
            return False
        LinkArc = CFArc()
        if( not pSlider1.GetSliderArc( LinkArc, true ) ):
            return False
        if( bOtherLinkHasSliders ):
            pass
#            SWAP( pSlider1, pLimit1 )
#            SWAP( pSlider2, pLimit2 )
        CommonCircle = LinkArc
        CommonCircle.r = self.Distance( CommonCircle.GetCenter(), pCommonConnector.GetPoint() )
        Intersect = CFPoint()
        Intersect2 = CFPoint()
        bHit = False
        bHit2 = False
        if( bOtherLinkOnly ):
            pTempLimit1 = 0
            pTempLimit2 = 0
            if( not pCommonConnector.GetSlideLimits( pTempLimit1, pTempLimit2 ) ):
                return False
            if( pCommonConnector.GetSlideRadius() == 0 ):
                bOnSegments = False
                Intersects( CFLine( pTempLimit1.GetTempPoint(), pTempLimit2.GetTempPoint() ),
                            CommonCircle, Intersect, Intersect2, bHit, bHit2, False, False )
            else:
                TheArc = CFArc()
                if( not pCommonConnector.GetSliderArc( TheArc, False ) ):
                    return False
                bHit = bHit2 = CommonCircle.CircleIntersection( TheArc, Intersect, Intersect2 )
        else:
            if( pFixedConnector == 0 ):
                return False
            r = self.Distance( pFixedConnector.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() )
            r = pLink.GetLinkLength( pFixedConnector, pCommonConnector )
            Circle = CFCircle(pFixedConnector.GetTempPoint(), r)
            bHit = bHit2 = CommonCircle.CircleIntersection( Circle, Intersect, Intersect2 )
        if( not bHit and not bHit2 ):
            return False
        if( not bHit2 ):
            Intersect2 = Intersect
        elif(not bHit):
            Intersect = Intersect2
        d1 = self.Distance( pCommonConnector.GetTempPoint(), Intersect )
        d2 = self.Distance( pCommonConnector.GetTempPoint(), Intersect2 )
        if( d2 < d1 ):
            Intersect = Intersect2
        if( not bOtherLinkOnly ):
            TempAngle = self.GetAngle( pFixedConnector.GetTempPoint(), Intersect, pFixedConnector.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() )
            TempAngle = self.GetClosestAngle( pFixedConnector.GetRotationAngle(), TempAngle )
            if( not pLink.RotateAround( pFixedConnector ) ):
                return False
            pLink.IncrementMoveCount( -1 )
        OriginalArc = CFArc()
        if(  not pSlider1.GetSliderArc( OriginalArc, True ) ):
            return False
        Offset = CFPoint(LinkArc.GetCenter() - OriginalArc.GetCenter())
        OrignalPoint = CFPoint(pCommonConnector.GetOriginalPoint())
        OrignalPoint += Offset
        Angle = self.GetAngle( LinkArc.GetCenter(), OrignalPoint, Intersect )
        pCommonConnector.MovePoint( Intersect )
        pCommonConnector.SetRotationAngle( -Angle )
        if( not pOtherLink.RotateAround( pCommonConnector ) ):
            return False
        if( not pActualSlider1.GetSliderArc( LinkArc ) ):
            pLink.ResetMoveCount()
            return False
        LinkArc2 = CFArc()
        if( not pActualSlider2.GetSliderArc( LinkArc2 ) ):
            pLink.ResetMoveCount()
            return False
        if( not LinkArc.PointOnArc( pActualSlider1.GetPoint() ) ):
            pSlider1.SetPositionValid( False )
            pLink.ResetMoveCount()
            return False
        if( not LinkArc2.PointOnArc( pActualSlider2.GetPoint() ) ):
            pSlider2.SetPositionValid( False )
            pLink.ResetMoveCount()
            return False
        return True
        
    def JoinToSlideLink(self, pLink, pFixedConnector, pCommonConnector, pOtherLink):
        if( pCommonConnector == 0 ):
            return False
        bOtherLinkOnly = ( pLink == pOtherLink and pFixedConnector == 0 )
        pLimit1 = 0
        pLimit2 = 0
        pSlider1 = 0
        pSlider2 = 0
        if( not pOtherLink.CanOnlySlide( pLimit1, pLimit2, pSlider1, pSlider2, bOtherLinkHasSliders ) ):
            return False
        if ( pSlider1.GetSlideRadius() != pSlider2.GetSlideRadius() ):
            return False
        if( pSlider1.GetSlideRadius() != 0 ):
            return self.JoinToSlideLinkSpecial( pLink, pFixedConnector, pCommonConnector, pOtherLink )
        if( pCommonConnector == pSlider1 or pCommonConnector == pSlider2 ):
            return False
        if( bOtherLinkHasSliders ):
            pass
            #SWAP( pSlider1, pLimit1 );
            #SWAP( pSlider2, pLimit2 );
        bSlidersAreMoving = pSlider1.HasLink( pLink )
        Angle = self.GetAngle( pSlider1.GetPoint(), pSlider2.GetPoint(), pSlider1.GetOriginalPoint(), pSlider2.GetOriginalPoint() )
        TempAngle = self.GetAngle( pLimit1.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() ) + Angle
        TempDistance = self.Distance( pLimit1.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() )
        EndPoint1 = CFPoint()
        EndPoint1.SetPoint( pSlider1.GetPoint(), TempDistance, TempAngle )
        TempAngle = self.GetAngle( pLimit2.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() ) + Angle
        TempDistance = self.Distance( pLimit2.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() )
        EndPoint2 = CFPoint()
        EndPoint2.SetPoint( pSlider2.GetPoint(), TempDistance, TempAngle )
        
        Intersect = CFPoint()
        Intersect2 = CFPoint()
        bHit = False
        bHit2 = False
        LimitLine = CFLine( EndPoint1, EndPoint2)
        if( bOtherLinkOnly ):
            pTempLimit1 = 0
            pTempLimit2 = 0
            if( not pCommonConnector.GetSlideLimits( pTempLimit1, pTempLimit2 ) ):
                return False
            if( pCommonConnector.GetSlideRadius() == 0 ):
                bOnSegments = False
                if(  Intersects( pTempLimit1.GetTempPoint(), pTempLimit2.GetTempPoint(),
                 EndPoint1, EndPoint2, Intersect, 0, bOnSegments or not bOnSegments ):
                    return False
                bHit = True
            else:
                TheArc = CFArc()
                if( not pCommonConnector.GetSliderArc( TheArc, False ) ):
                    return False
                Intersects( LimitLine, TheArc, Intersect, Intersect2, bHit, bHit2, False, False )
                if( not bHit and not bHit2 ):
                    return False
                if( not TheArc.PointOnArc( Intersect2 ) ):
                    Intersect2 = Intersect
                    if( not TheArc.PointOnArc( Intersect ) ):
                        return False
        else:
            if( pFixedConnector == 0 ):
                return False
            r = self.Distance( pFixedConnector.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() )
            r = pLink.GetLinkLength( pFixedConnector, pCommonConnector )
            Circle = CFCircle(pFixedConnector.GetTempPoint(), r)
            Intersects( LimitLine, Circle, Intersect, Intersect2, bHit, bHit2, False, False )
        if( not bHit and not bHit2 ):
            return False
        if not bHit2 :
            Intersect2 = Intersect
        elif not bHit:
            Intersect = Intersect2
        d1 = self.Distance( pCommonConnector.GetTempPoint(), Intersect )
        d2 = self.Distance( pCommonConnector.GetTempPoint(), Intersect2 )
        if( d2 < d1 ):
            Intersect = Intersect2
        if( not bOtherLinkOnly ):
            TempAngle = self.GetAngle( pFixedConnector.GetTempPoint(), Intersect, pFixedConnector.GetOriginalPoint(), pCommonConnector.GetOriginalPoint() )
            TempAngle = self.GetClosestAngle( pFixedConnector.GetRotationAngle(), TempAngle )
            pFixedConnector.SetRotationAngle( TempAngle )
            if( not pLink.RotateAround( pFixedConnector ) ):
                return False
        pLink.IncrementMoveCount( -1 )
        pCommonConnector.MovePoint( Intersect )
        Angle = self.GetClosestAngle( pCommonConnector.GetRotationAngle(), Angle )
        pCommonConnector.SetRotationAngle( Angle )
        if( not pOtherLink.RotateAround( pCommonConnector ) ):
            return False
        return True
    def SlideToLink(self, pLink, pFixedConnector, pSlider, pLimit1, pLimit2):
        ###testslidetoLink
            
        
        
            
        
        
        
        
                
            
                
                
                
        
    
    
