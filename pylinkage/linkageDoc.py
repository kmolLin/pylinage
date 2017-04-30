from Connector import CConnector
from link import CLink
from ControlKnob import CControlKnob

class CLinkageDoc(list):
    def __init__(self):
        self.m_pCapturedConnector = 0
        self.m_pCapturedConrolKnob = 0
        self.m_pUndoList = 0
        self.m_pUndoListEnd = 0
        self.m_UndoCount = 0

        self.m_bSelectionMakeAnchor = False
        self.m_bSelectionConnectable = False
        self.m_bSelectionCombinable = False
        self.m_bSelectionJoinable = False
        self.m_bSelectionSlideable = False
        self.m_bSelectionSplittable = False
        self.m_bSelectionTriangle = False
        self.m_bSelectionRectangle = False
        self.m_bSelectionLineable = False
        self.m_bSelectionFastenable = False
        self.m_bSelectionUnfastenable = False
        self.m_bSelectionLockable = False
        self.m_bSelectionMeshable = False
        self.m_bSelectionPositionable = False
        self.m_bSelectionLengthable = False
        self.m_bSelectionRotatable = False
        self.m_bSelectionScalable = False

        self.m_AlignConnectorCount = 0
        self.m_HighestConnectorID = -1
        self.m_HighestLinkID = -1
        self.m_UnitScaling = 1
        self.m_SelectedLayers = 0
        self.m_ScaleFactor = 1.0
    def SelectElement(self, *keyword):
        if len(keyword)==0:
            self.ClearSelection()
        elif type(keyword[0])==CConnector:
            if( keyword[0].IsSelected() ):
                return False
            self.m_SelectedConnectors.append(keyword[0])
            keyword[0].Select(True)
            self.m_SelectedConnectors =keyword[0]
            return True
        elif type(keyword[0])==CLink:
            pass
        ### not yet to do
    def InsertLink(self, Layers, ScaleFactor, DesiredPoint, bForceToPoint, 
    ConnectorCount,bAnchor,bRotating,bSlider,bActuator,bMeasurement,bSolid,bGear):
        if( self.ConnectorCount == 0 ):
            return
        MAX_CONNECTOR_COUNT = 4
        '''
        * right now, there is no clever way to generate the location for
        * the new connectors so 3 is the maximum.
        '''
        if ( ConnectorCount > MAX_CONNECTOR_COUNT ):
            return
        self.ClearSelection()  ##notice
        def AddPoints(): return [
            [CFPoint(0, 0), CFPoint(0, 0), CFPoint(0, 0), CFPoint(0, 0)],
            [CFPoint(0, 0), CFPoint(1., 1.), CFPoint(0, 0), CFPoint(0, 0)],
            [CFPoint(0, 0), CFPoint(0, 1.), CFPoint(1., 1.), CFPoint(0, 0)],
            [CFPoint(0, 0), CFPoint(0, 1.), CFPoint(1., 1.), CFPoint(1., 0)],
            ]
        Connectors = CConnector(ConnectorCount)
        if( Connectors == 0 ):
            return
        ###3718

