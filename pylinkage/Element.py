from ControlKnob import CControlKnob

class CElementItem:
    CONNECTOR = 0
    LINK = 1
    NONE = 2
    def __init__(self, **Args):
        if Args.get('pLink', None)!=None:
            self.m_ElementType = self.LINK
            self.pElement = CElement(Args['pLink'])
        elif Args.get('pConnector', None)!=None:
            self.m_ElementType = self.CONNECTOR
            self.pElement = CElement(Args['pConnector'])
        else:
            self.m_ElementType = self.NONE
            self.pElement = 0
    
    def GetLink(self): return CLink(self.pElement) if self.m_ElementType==self.LINK else 0
    def GetConnector(self): return CConnector(self.pElement) if self.m_ElementType==self.CONNECTOR else 0
    def GetElement(self): return CElement(self.pElement)

class ElementList(list):
    def Remove(self, pElement):
        try:
            self.remove(pElement)
            return True
        except ValueError: return False
    def __getitem__(self, k):
        if len(self)==0:
            print('error')
        else:
            return self[k]

class CElement():
    def __init__(self, ExistingElement=None):
        self.m_FastenedElements = ElementList()
        self.m_ControlKnob = CControlKnob()
        if ExistingElement !=None:
            self.m_Identifier = -1  # Should never copy and ID but some value needs to be set here.
            self.m_bSelected = ExistingElement.m_bSelected
            self.m_Layers = ExistingElement.m_Layers
            self.m_Name = ExistingElement.m_Name
            self.m_bMeasurementElement = ExistingElement.m_bMeasurementElement
            self.m_bPositionValid = ExistingElement.m_bPositionValid
            self.m_Color = ExistingElement.m_Color
            self.m_FastenedTo = CElementItem()
        else:
            self.m_bSelected = False
            self.m_Layers = 0
            self.m_bMeasurementElement = False
            self.m_bPositionValid = True
            self.m_FastenedTo = CElementItem()
    
    def SetName(self, pName): self.m_Name = pName
    
    def GetName(self): return self.m_Name
    
    def IsSelected(self): return self.m_bSelected
    
    def Select(self, bSelected): self.m_bSelected = bSelected
    
    def SetIdentifier(self, Value): self.m_Identifier = Value
    
    def GetIdentifier(self): return self.m_Identifier
    
    def GetIdentifierString(self, bDebugging): return 0
    
    def GetTypeString(self):
        bDrawingLayer = self.GetLayers() and CLinkageDoc.DRAWINGLAYER
        if self.IsMeasurementElement(): return "Measurement"
        if self.IsConnector():
            if self.bDrawingLayer:
                if CConnector(self).GetDrawCircleRadius() > 0: return "Circle"
                else: return "Point"
            elif CConnector(self).IsAnchor(): return "Anchor"
            else: return "Connector"
        else:
            if self.bDrawingLayer: return "Polyline"
            elif CLink(self).IsActuator(): return "Actuator"
            elif CLink(self).IsGear(): return "Gear"
            else: return "Link"
    
    def SetLayers(self, Layers): self.m_Layers = Layers
    
    def GetLayers(self): return self.m_Layers
    
    def IsOnLayers(self, Layers): (self.m_Layers and Layers)!=0
    
    def SetMeasurementElement(self, bSet): self.m_bMeasurementElement = bSet
    
    def IsMeasurementElement(self): return self.m_bMeasurementElement
    
    def SetPositionValid(self, bSet):self.m_bPositionValid = bSet
    
    def IsPositionValid(self): return self.m_bPositionValid
    
    def GetColor(self): return self.m_Color
    
    def SetColor(self, Color): self.m_Color = Color
    
    def GetFastenedTo(self): return 0 if self.m_FastenedTo.GetElement()==0 else CElementItem(self.m_FastenedTo)
    
    def GetFastenedToLink(self): return 0 if self.m_FastenedTo.GetLink() == 0 else CLink(self.m_FastenedTo.GetLink())
    def GetFastenedToConnector(self): return 0 if self.m_FastenedTo.GetConnector() == 0 else CConnector(self.m_FastenedTo.GetConnector())
    
    def UnfastenTo(self):
        pItem = self.GetFastenedTo()
        if pItem !=0 and pItem.GetElement() !=0:
            pItem.GetElement().RemoveFastenElement(self)
        self.m_FastenedTo = CElementItem()
        
    def FastenTo(self, pFastenLink): self.m_FastenedTo = pFastenLink
    
    def GetFastenedElementList(self): return self.m_FastenedElements
    
    def AddFastenConnector(self, pConnector):
        self.m_FastenedElements.append(CElementItem(pConnector))
    def AddFastenLink(self, pLink):
        self.m_FastenedElements.append(CElementItem(pLink))
    def RemoveFastenElement(self, pElement):
        Position = self.m_FastenedElements[0]
        while(Position != 0 ):
            DeletePosition = Position
            pItem = CElementItem(self.m_FastenedElements[Position+1])
            if pItem == 0:continue
            if pItem.GetElement() ==  pElement  or pElement ==0:
                del self.m_FastenedElements[DeletePosition]
                if pItem.GetElement().GetFastenedTo()!= 0 and self ==pItem.GetElement().GetFastenedTo().GetElement():
                    pItem.GetElement().UnfastenTo()
                break
    def IsLink(self):return 0
    def IsConnector(self): return 0
    def GetControlKnob(self):return 1 # self.m_ControlKnob()
    def GetLocation(self):return 0
    def UpdateControlKnob(self, Point=None):return 0

    
    
    
