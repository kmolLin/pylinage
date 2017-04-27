##geometry
from math import *


def Distance(Point1,Point2):
    if type(Point1) == CFPoint and type(Point2) == CFPoint:
        return sqrt(abs((Point1.x - Point2.x)**2)+abs((Point1.y - Point2.y)**2))
    else:
        raise TypeError("Wrong Type.")
        
def GetAngle(*keyword):
    if len(keyword) ==2:
        Angle =  degrees(atan2( keyword[1].y - keyword[0].y, keyword[1].x - keyword[0].x )) 
        if Angle <0:
            Angle +=360
        return Angle
    elif len(keyword) ==3:
        Angle1 = degrees(atan2(keyword[1].y-keyword[0].y, keyword[1].x-keyword[0].x))
        Temp = atan2(keyword[1].y-keyword[0].y, keyword[1].x-keyword[0].x)
        Angle2 = degrees(atan2(keyword[2].y-keyword[0].y, keyword[2].x-keyword[0].x))
        if Angle1 <-180 :
            Angle1 +=360
        if Angle2 < -180:
            Angle2 +=360
        Angle = Angle1-Angle2
        return Angle
    elif len(keyword) ==4:
        Angle1 = degrees(atan2(keyword[1].y-keyword[0].y, keyword[1].x-keyword[0].x))
        Angle2 = degrees(atan2(keyword[3].y-keyword[2].y, keyword[3].x-keyword[2].x))
        if Angle1 <-180:
            Angle1+=360
        if Angle2 <-180:
            Angle2 +=360
        Angle = Angle1 -Angle2
        return Angle
        
        

def setprecision(x, prec):
    #return ceil( x * pow( 10, (double)prec ) - .4999999999999) / pow(10,(double)prec );
    return 
    
def DistanceToLine(End1, End2, CheckPoint):
    r_numerator = (CheckPoint.x-End1.x)*(End2.x-End1.x) + (CheckPoint.y-End1.y)*(End2.y-End1.y)
    r_denomenator = (End2.x-End1.x)*(End2.x-End1.x) + (End2.y-End1.y)*(End2.y-End1.y)
    r = r_numerator / r_denomenator
    px = End1.x + r*(End2.x-End1.x)
    py = End1.y + r*(End2.y-End1.y)
    s =  ((End1.y-CheckPoint.y)*(End2.x-End1.x)-(End1.x-CheckPoint.x)*(End2.y-End1.y) ) / r_denomenator
    DistanceToLine = abs(s)*sqrt(r_denomenator)
    DistanceToSegment = 0
    xx = px
    yy = py
    if r >= 0 and r <= 1:
        DistanceToSegment = DistanceToLine
    else:
        dist1 = (CheckPoint.x-End1.x)*(CheckPoint.x-End1.x) + (CheckPoint.y-End1.y)*(CheckPoint.y-End1.y)
        dist2 = (CheckPoint.x-End2.x)*(CheckPoint.x-End2.x) + (CheckPoint.y-End2.y)*(CheckPoint.y-End2.y)
        if dist1 < dist2:
            xx = End1.x
            yy = End1.y
            DistanceToSegment = sqrt(dist1)
        else:
            xx = End2.x
            yy = End2.y
            DistanceToSegment = sqrt(dist2)
        return DistanceToSegment
    
def Intersects(*keyword):
    if type(keyword[1]) == CFCircle:
        Line = keyword[0]
        Circle = keyword[1]
        HitPoint1 = keyword[2]
        HitPoint2 = keyword[3]
        bHit1 = keyword[4]
        bHit2 = keyword[5]
        bBeforeOkay = keyword[6]
        bAfterOkay = keyword[7]

        dx = keyword[0][1].x - keyword[0][0].x
        dy = keyword[0][1].y - keyword[0][0].y
        
        keyword[4] =True
        keyword[5] =True
        drsq = dx * dx + dy * dy
        D = ( keyword[0][0].x - keyword[1].x ) * dy - ( keyword[0][0].y - keyword[1].y ) * dx
        if (keyword[1].r*keyword[1].r*drsq -D**2)<0:
            keyword[4] =False
            keyword[5] =False
            return
        else:
            det = sqrt(keyword[1]**2*drsq-(D**2))
            keyword[2].x =  keyword[1].x+( D * dy + dx * det) / drsq
            keyword[2].y =  keyword[1].y+( (-D) * dx + dy * det) / drsq
            keyword[3].x =  keyword[1].x+( D * dy + dx * det) / drsq
            keyword[3].y =  keyword[1].y+( (-D) * dx + dy * det) / drsq
            d = keyword[0].x+dx
            d2 = keyword[0].y+dy
            xsign = copysign(1, keyword[0][1].x-keyword[0][0].x)
            ysign = copysign(1, keyword[0][1].y-keyword[0][0].y)
            
            if d - keyword[0][1].x <-0.00005 or d - keyword[0][1].x>0.00005:
                keyword[4] =False
                keyword[5] =False
                return
            #If the line is dead vertical or horizontal then the hit point MUST be
            #on that same x or y coordinate. Rounding of IEEE numbers can be off
            #sometimes and then the intersection is incorrectly rejected.
            if keyword[0][0].x ==keyword[0][1].x:
                keyword[2].x = keyword[0].x 
                keyword[3].x = keyword[0].x
            if keyword[0][0].y ==keyword[0][1].y:
                keyword[2].y = keyword[0].y 
                keyword[3].y = keyword[0].y
            
            Fudge = 10000.0
            
            if not bBeforeOkay:
                if( copysign( 1, HitPoint1.x - Line[0].x ) != xsign ):
                    if floor( HitPoint1.x * Fudge ) != floor( Line[0].x * Fudge ):
                        bHit1 = false
                if ( copysign( 1, HitPoint1.y - Line[0].y ) != ysign ):
                    if ( floor( HitPoint1.y * Fudge ) != floor( Line[0].y * Fudge ) ):
                        bHit1 = false
                if( copysign( 1, HitPoint2.x - Line[0].x) != xsign ):
                    if( floor( HitPoint2.x * Fudge ) != floor( Line[0].x * Fudge ) ):
                        bHit2 = false
                if ( copysign( 1, HitPoint2.y - Line[0].y) != ysign ):
                    if( floor( HitPoint2.y * Fudge ) != floor( Line[0].y * Fudge ) ):
                        bHit2 = false
            if not bAfterOkay:
                if( copysign( 1, Line[1].x - HitPoint1.x  ) != xsign ):
                    if( floor( HitPoint1.x * Fudge ) != floor( Line[1].x * Fudge ) ):
                        bHit1 = false;
                if( copysign( 1, Line[1].y - HitPoint1.y ) != ysign ):
                    if( floor( HitPoint1.y * Fudge ) != floor( Line[1].y * Fudge ) ):
                        bHit1 = false
                if ( _copysign( 1, Line[1].x - HitPoint2.x ) != xsign ):
                    if( floor( HitPoint2.x * Fudge ) != floor( Line[1].x * Fudge ) ):
                        bHit2 = false
                if ( _copysign( 1, Line[1].y - HitPoint2.y ) != ysign ):
                    if( floor( HitPoint2.y * Fudge ) != floor( Line[1].y * Fudge ) ):
                        bHit2 = false
    elif type(keyword[1]) == CFLine:
        return (keyword[0][0],keyword[0][1], keyword[1][0],keyword[1][1],keyword[2], keyword[3]
            , keyword[4], keyword[5])
    elif type(keyword[1]) == CFPoint:
        line1Point1 = keyword[1]
        line1Point2 = keyword[2]
        line2Point1 = keyword[3]
        line2Point2 = keyword[4]
        intersection = keyword[5]
        pDirection = keyword[6]
        pbOnBothSegments = keyword[7]
        pbOnFirstSegment = keyword[8]
        '''
        Based on the 2d line intersection method from "comp.graphics.algorithms
        Frequently Asked Questions"
        (Ay-Cy)(Dx-Cx)-(Ax-Cx)(Dy-Cy)
        r = ----------------------------- (eqn 1)
        (Bx-Ax)(Dy-Cy)-(By-Ay)(Dx-Cx)
        '''


        q =	(( line1Point1.y - line2Point1.y ) * (line2Point2.x - line2Point1.x) -
            (line1Point1.x - line2Point1.x) * (line2Point2.y - line2Point1.y))
            
        d =	((line1Point2.x - line1Point1.x) * (line2Point2.y - line2Point1.y) -
                (line1Point2.y - line1Point1.y) * (line2Point2.x - line2Point1.x))
                
        if d == 0:
            return False
        r = q / d
        if pDirection != None:
            pDirection = 1 if r >= 0 else 0
            q = ((line1Point1.y - line2Point1.y) * (line1Point2.x - line1Point1.x) -
                (line1Point1.x - line2Point1.x) * (line1Point2.y - line1Point1.y))
            s = q / d
        if  pbOnBothSegments != None:
            if( r < 0 or r > 1 or s < 0 or s > 1 ):
                pbOnBothSegments = False
                if( pbOnFirstSegment != None ):
                    if( s < 0 or s > 1 ):
                        pbOnFirstSegment = False
                    else:
                        pbOnFirstSegment = True
                else:
                    pbOnBothSegments = True
                    if( pbOnFirstSegment != None):
                        pbOnFirstSegment = True
        if pbOnFirstSegment != Nnoe:
            if( r < 0 or r > 1 ):
                pbOnFirstSegment = false
            else:
                pbOnFirstSegment = True
                
        intersection.x = line1Point1.x + ( r * (line1Point2.x - line1Point1.x))
        intersection.y = line1Point1.y + ( r * (line1Point2.y - line1Point1.y))
        return True

def DistanceAlongLine(Line, Point):
    AP = CFPoint(Point - Line.GetStart())
    AB = CFPoint(Line.GetEnd() - Line.GetStart())
    ab2 = AB.x*AB.x + AB.y*AB.y
    ap_ab = AP.x*AB.x + AP.y*AB.y
    t = ap_ab / ab2
    TempLine = CFLine(CFPoint( 0, 0 ), AB)
    Distance = TempLine.GetDistance() * t
    return Distance

class CFPoint():
    def __init__(self, *keyword):
        if len(keyword)==2:
            self.x = keyword[0]
            self.y = keyword[1]
        elif len(keyword)==1:
            self.x = keyword[0].x
            self.y = keyword[0].y
        else:
            self.x = 0.
            self.y = 0.
    
    def DistanceToPoint(self, **Args):
        if Args.get('Point', None)!=None:
            Point = Args['Point']
            return sqrt((Point.x-self.x)**2+(Point.y-self.y)**2)
        elif Args.get('x', None)!=None and Args.get('y', None)!=None:
            x = Args['x']
            y = Args['y']
            return sqrt((x-self.x)**2+(y-self.y)**2)
    
    def __sub__(self, Right): return CFPoint(self.x-Right.x, self.y-Right.y)
    def __add__(self, Right): return CFPoint(self.x+Right.x, self.y+Right.y)
    def __truediv__(self, f): return CFPoint(self.x/f, self.y/f)
    def __isub__(self, Right):
        if type(Right)==float:
            self.x-=Right
            self.y-=Right
        else:
            self.x-=Right.x
            self.y-=Right.y
    def __eq__(self, Right): return self.x==Right.x and self.y==Right.y
    def __ne__(self, Right): return self.x!=Right.x or self.y!=Right.y
    def __iconcat__(self, Right):
        if type(Right)==float:
            self.x+=Right
            self.y+=Right
        else:
            self.x+=Right.x
            self.y+=Right.y
    
    def __str__(self): return "<Point x={v.x} y={v.y}>".format(v=self)
    
    def SetPoint(self, *keyword):
        if len(keyword)==1:
            Point = keyword[0]
            self.x = Point.x
            self.y = Point.y
        elif len(keyword)==2:
            self.x = keyword[0]
            self.y = keyword[1]
        elif len(keyword)==3:
            Angle = radians(keyword[2])
            self.x = keyword[0].x + (keyword[1] * cos(Angle))
            self.y = keyword[0].y + (keyword[1] * sin(Angle))
    
    def IsInsideOf(self, Rect): return (self.y>=Rect.top and self.y<=Rect.bottom and
        self.x>=Rect.left and self.x<=Rect.right)
    
    def SnapToLine(self, Line, bToSegment, bStartToInfinity = False):
        AP = self - Line.GetStart()
        AB =Line.GetEnd() - Line.GetStart()
        ab2 = AB.x**2+AB.y**2
        ap_ab = AP.x*AB.x+AP.y*AB.y
        t = ap_ab / ab2
        if(bToSegment or bStartToInfinity ):
            if t < 0.0:
                t = 0.0
            elif -bStartToInfinity and t > 1.0:
                t = 1.0
        self.x = Line.m_Start.x + AB.x * t
        self.y = Line.m_Start.y + AB.y * t
        
    def SnapToArc(self, TheArc ):
        AngleLine = CFLine(TheArc.x,TheArc.y, self.x, self.y)
        AngleLine.SetDistance(abs( TheArc.r ))
        Point = CFPoint(AngleLine.GetEnd())
        if TheArc.GetStart() != TheArc.GetEnd() and -TheArc.PointOnArc( Point ):
            d1 = Distance(TheArc.GetStart(), Point)
            d2 = Distance( TheArc.GetEnd(), Point )
            if d1 <= d2:
                Point = TheArc.GetStart()
            else:
                Point = TheArc.GetEnd()
            self = Point    
            return Point
    def GetDistance(self, Point): return sqrt((Point.x-x)**2+(Point.y-y)**2)
    
    def MidPoint(self, OtherPoint, ScaleDistance):
        Line = CFLine(self, Point)
        Line.SetDistance(Line.GetDistance()*ScaleDistance)
        return Line.GetEnd()
    def RotateAround(self, OtherPoint, Angle):
        Angle = radians(Angle)
        x1 = self.x - OtherPoint.x
        y1 = self.y - OtherPoint.y
        Cosine = cos( Angle )
        Sine = sin( Angle )
        x2 = x1 * Cosine - y1 * Sine
        y2 = x1 * Sine + y1 * Cosine
        self.x = x2 + OtherPoint.x
        self.y = y2 + OtherPoint.y
        
class CFLine():
    def __init__(self, *keyword):
        self.m_Start = CFPoint()
        self.m_End = CFPoint()
        if len(keyword)==4: self.SetLine(keyword[0], keyword[1], keyword[2], keyword[3])
        elif len(keyword)==2: self.SetLine(keyword[0].x, keyword[0].y, keyword[1].x, keyword[1].y)
        elif len(keyword)==1: self.SetLine(keyword[0])
        else: self.SetLine(0, 0, 0, 0)
        
    def SetLine(self, *keyword):
        if len(keyword)==4:
            self.m_Start.x = keyword[0]
            self.m_Start.y = keyword[1]
            self.m_End.x = keyword[2]
            self.m_End.y = keyword[3]
        elif len(keyword) ==2:
            self.m_Start.x = keyword[0].x
            self.m_Start.y = keyword[0].y
            self.m_End.x = keyword[1].x
            self.m_End.y = keyword[1].y
        elif len(keyword)==1:
            self.m_Start.x = keyword[0][0].x
            self.m_Start.y = keyword[0][0].y
            self.m_End.x = keyword[0][1].x
            self.m_End.y = keyword[0][1].y
    def SetDistance(self, Distance):
        if self.m_End.x ==self.m_Start.x and self.m_End.y == self.m_Start.y:return
        ScaleFactor = Distance/sqrt((self.m_End.x-self.m_Start.x)**2+(self.m_End.y-self.m_Start.y)**2)
        self.m_End.x = self.m_Start.x + (self.m_End.x - self.m_Start.x)*ScaleFactor
        self.m_End.y = self.m_Start.y + (self.m_End.y - self.m_Start.y)*ScaleFactor
        
    def GetDistance(self):
        return sqrt((self.m_End.x - self.m_Start.x)**2+(self.m_End.y - self.m_Start.y)**2)
        
    def GetAngle(self):
        return degrees(atan2(self.m_End.y-self.m_Start.y, self.m_End.x-self.m_Start.x))
        
    def GetParallelLine(self, NewLine, Offset):
        if Offset ==0:
            NewLine.SetLine(self)
            return
        Length = self.GetDistance()
        dx  = (self.m_End.x - self.m_Start.x)*abs(Offset)/Length
        dy  = (self.m_End.y - self.m_Start.y)*abs(Offset)/Length
        
        if( Offset > 0 ):
            dy = -dy
        else:
            dx = -dx
        NewLine.SetLine(self.m_Start.x+dy,self.m_Start.y+dx,self.m_End.x+dy,self.m_End.y+dx) 
    
    def ReverseDirection(self): self.m_Start, self.m_End = self.m_End, self.m_Start
    
    def __str__(self):return "<Line start={v.m_Start} end={v.m_End}>".format(v = self)
    
    def __getitem__(self, Index): return self.m_Start if Index==0 else self.m_End
    
    def __isub__(self, Right):self.SetLine(self.m_Start.x-Right.x, self.m_Start.y-Right.y, 
        self.m_End.x-Right.x, self.m_End.y-Right.y)
    def __iadd__(self, Right):self.SetLine(self.m_Start.x+Right.x, self.m_Start.y+Right.y, 
        self.m_End.x+Right.x, self.m_End.y+Right.y)
    def PerpendicularPoint(self, Perp, Direction = 1):
        dx = self.m_End.x - self.m_Start.x
        dy = self.m_End.y - self.m_Start.y
        if( Direction == 1 ):
            Perp.SetPoint(self.m_End.x-dy, self.m_End.y+dx)
        else:
            Perp.SetPoint(self.m_End.x+dy, self.m_End.y-dx)
            
    def PerpendicularLine(self,*keyword):
        if len(keyword)==2:
            Point  = self.m_End
            PerpendicularPoint(keyword[0][1], keyword[1])
            keyword[0][0] = Point  ####
        elif len(keyword)==3:
            Point = self.m_End;
            PerpendicularPoint( keyword[0][1], keyword[2]);
            keyword[0][0] = Point;
            keyword[0].SetDistance( keyword[1]);
            
    def MoveEnds(self, MoveStartDistance, MoveEndDistance):
        if self.m_End.x ==self.m_Start.x and self.m_End.y ==self.m_Start.y:
            return
        Length = sqrt((self.m_End.x-self.m_Start.x)**2+(self.m_End.y-self.m_Start.y)**2)
        ScaleFactor = MoveStartDistance / Length
        self.m_Start.x = self.m_Start.x + ((self.m_End.x-self.m_Start.x)*ScaleFactor)
        self.m_Start.y = self.m_Start.y + ((self.m_End.y-self.m_Start.y)*ScaleFactor)
        ScaleFactor = MoveEndDistance / Length
        self.m_End.x = self.m_End.x + ((self.m_End.x-self.m_Start.x)*ScaleFactor)
        self.m_End.y = self.m_End.y + ((self.m_End.y-self.m_Start.y)*ScaleFactor)
        
    def MoveEndsFromStart(self, MoveStartDistance, MoveEndDistance):
        if self.m_End.x == self.m_Start.x and self.m_End.y ==self.m_Start.y:
            return
        Length = sqrt((self.m_End.x-self.m_Start.x)**2+(self.m_End.y-self.m_Start.y)**2)
        ScaleFactor = MoveStartDistance / Length
        NewStart = CFPoint()
        NewStart.x = self.m_Start.x + ((self.m_End.x - self.m_Start.x)*ScaleFactor)
        NewStart.y = self.m_Start.y + ((self.m_End.y - self.m_Start.y)*ScaleFactor)
        ScaleFactor = MoveEndDistance / Length
        NewEnd = CFPoint()
        NewEnd.x = self.m_Start.x + ((self.m_End.x - self.m_Start.x)*ScaleFactor)
        NewEnd.y = self.m_Start.y + ((self.m_End.y - self.m_Start.y)*ScaleFactor)
        
        self.m_Start = NewStart
        self.m_End = NewEnd
    def MidPoint(self, ScaleDistance):
        Line = CFLine(self.m_Start, self.m_End)
        Line.SetDistance(Line.GetDistance() * ScaleDistance)
        return Line.GetEnd()
        
    def GetStart(self): return self.m_Start
    def GetEnd(self): return self.m_End
    
class CFCircle():
    def __init__(self, *keyword):
        ## (CFPoint,R) ##(x,y,r)
        self.SetCircle(*keyword)
    
    def SetCircle(self, *keyword):
        if len(keyword) == 2:
            Center = keyword[0]
            if type(keyword[1])==float:
                self.x = Center.x
                self.y = Center.y
                self.r = keyword[1]
            else:
                r = Distance(Center, keyword[1])
                self.x = Center.x
                self.y = Center.y
                self.r = r
        elif len(keyword) == 3:
            self.x = keyword[0] 
            self.y = keyword[1]
            self.r = keyword[2]
        else:
            self.x = 0.
            self.y = 0.
            self.r = 0.
    def GetCenter(self):return (self.x, self.y)
    
    def CircleIntersection(self, OtherCircle, ReturnPoint0, ReturnPoint1):
        ##
        p2 = CFPoint()
        p3 = CFPoint()
        d = sqrt((OtherCircle.x - self.x)**2, (OtherCircle.y - self.y)**2)
        a = ((self.r*self.r)-(OtherCircle.r**2)+(d*d)/(d+d))
        if abs(a) >abs(r):
            if abs(a)-r>0.00005:
                return False
            a = r*(1 if a>=0 else -1)
            
        h = sqrt(r**2-a**2)
        p2.x =x + a * ( OtherCircle.x - x ) / d
        p2.y = y + a * ( OtherCircle.y - y ) / d
        p3.x = p2.x + h * ( OtherCircle.y - y ) / d
        p3.y = p2.y - h * ( OtherCircle.x - x ) / d
        ReturnPoint0 = p3
        p3.x = p2.x - h * ( OtherCircle.y - y ) / d
        p3.y = p2.y + h * ( OtherCircle.x - x ) / d
        ReturnPoint1 = p3
        return True
        
class CFArc(CFCircle):
    def __init__(self, *keyword):
        ##CFPoint &Center, double Radius, CFPoint &Start, CFPoint &End
        ##double x, double y, double Radius, CFPoint &Start, CFPoint &End
        ##()
        if len(keyword) ==0:
            pass
        elif len(keyword) == 4:
            self.SetArc(keyword[0], keyword[1],keyword[2],keyword[3])
        elif len(keyword) ==5:
            self.SetArc(CFPoint(keyword[0], keyword[1]),keyword[2],keyword[3],keyword[4])
    def SetArc(self, Center, Radius, Start, End):
        self.x = Center.x
        self.y = Center.y
        self.r = Radius
        self.m_Start = Start
        self.m_End = End
    def __eq__(self, Right): return (self.x == Right.x and self.y == Right.y and self.r == Right.r and
        self.m_Start == Right.m_Start and self.m_End == Right.m_End)
        
    def GetStart(self):return self.m_Start
    def GetEnd(self): return self.m_End
    
    def GetStartAngle(self): return degrees(atan2(self.m_Start.y- self.y, self.m_Start.x-self.x))
    def GetEndAngle(self):return degrees(atan2(self.m_End.y - self.y, self.m_End.x - self.x))
    def __str__(self):return "<Arc center={v.x},{v.y} r={v.r} Start={v.m_Start} end={v.m_End}>".format(v = self)
    def PointOnArc(self, Point):
        Distance = self.Distance(CFPoint(self.x, self.y), Point)
        StartAngle = GetAngle(CFPoint(self.x, self.y), self.m_Start)
        EndAngle = GetAngle(CFPoint(self.x, self.y), self.m_End)
        if( EndAngle < StartAngle ):EndAngle += 360.0
        if( Angle < StartAngle ):Angle += 360
        return Angle >= StartAngle and Angle <= EndAngle
        
    def AngleSpan(self):
        Angle = GetStartAngle()
        EndAngle = GetEndAngle()
        if( Angle == EndAngle ):
            Angle = 0
        elif Angle > EndAngle:
            Angle =((360-Angle)+EndAngle)/2
        else:
            Angle=(EndAngle-Angle)/2
        return Angle
        
class CFRect():
    def __init__(self, *keyword):
        if len(keyword) ==4:
            self.top = keyword[0]
            self.left = keyword[1]
            self.bottom = keyword[2]
            self.right = keyword[3]
        elif len(keyword) ==1:
            self.top = keyword[0].top
            self.left = keyword[0].left
            self.bottom = keyword[0].bottom
            self.right = keyword[0].right
        elif len(keyword) ==2:
            self.top = keyword[0].y
            self.left = keyword[0].x
            self.bottom = keyword[1].y
            self.right = keyword[1].x
        else:
            self.top = 0.
            self.left = 0.
            self.bottom = 0.
            self.right = 0.
            
        def SetRect(self, *keyword):
            if len(keyword) ==4:
                self.top = keyword[1]
                self.left = keyword[3]
                self.bottom = keyword[0]
                self.right = keyword[2]
                
            elif len(keyword) ==2:
                self.top = keyword[0].y
                self.bottom = keyword[1].y
                self.left = keyword[0].x
                self.right = keyword[1].x
        def InflateRect(self, x, y):
            self.top-=y
            self.top-=x
            self.bottom+=y
            self.bottom+=x
            
        def __iadd__(self, Point):
            self.top += Point.y
            self.bottom += Point.y
            self.left += Point.x
            self.right += Point.x
        def IsOverlapped(self, Rect):
            return (Rect.top>self.bottom or Rect.bottom<self.top or 
            Rect.left > self.right or Rect.right < self.left)
            
        def IsInsideOf(self, Rect):
            return ( self.top >= Rect.top and self.top <= Rect.bottom
            and self.bottom >= Rect.top and self.bottom <= Rect.bottom
            and self.left >= Rect.left and self.left <= Rect.right
            and self.right >= Rect.left and self.right <= Rect.right )
            
        def PointInRect(self, Point):
            return (Point.x >= self.left and Point.y >= self.top and 
            Point.x < self.right and Point.y < self.bottom)
            
        def GetCenter(self):
            CFPoint((self.left+self.right)/ 2,(self.top+self.bottom)/2 )
            
        def Width(self): return self.right-self.left
        def Height(self): return self.bottom-self.top
        
        def TopLeft(self): return CFPoint( self.left, self.top )
        def BottomRight(self): return CFPoint( self.right, self.bottom )
        def TopRight(self): return CFPoint( self.right, self.top )
        def BottomLeft(self): return CFPoint( self.left, self.bottom )
        
        def Normalize(self):
            if self.top >self.bottom:
                self.top, self.bottom = self.bottom, self.top
            if self.left>self.right:self.left, self.right = self.right, self.left
            
class CFArea(CFRect):
    def __init__(self, *keyword):
        if len(keyword) == 1 :
            self.top = keyword[0].top
            self.left = keyword[0].left
            self.bottom = keyword[0].bottom
            self.right = keyword[0].right
        elif len(keyword) == 4 :
            self.top = keyword[0]
            self.left = keyword[1]
            self.bottom = keyword[2]
            self.right = keyword[3]
        elif len(keyword) == 2 :
            self.top = keyword[0].y
            self.left = keyword[0].x
            self.bottom = keyword[1].y
            self.right = keyword[1].x
        else :
            self.top = nan
            self.left = nan
            self.bottom = nan
            self.right = nan
            
        def IsValid(): return not isnan(self.left)
        
        def GetRect():return CFRect(self.left,self.top,self.right,self.bottom) if self.IsValid() else CFRect()
            
        def __isub__(self, Point):
            if type(Point) == CFPoint:
                if  not self.IsValid():
                    self.top = Point.y
                    self.bottom = Point.y
                    self.left = Point.x
                    self.right = Point.x
                    return
                self.top = min(self.top, Point.y)
                self.bottom = max(self.bottom, Point.y)
                self.left = min(self.left, Point.x)
                self.right = max(self.right, Point.x)
            elif type(Point) == CFRect:
                Rect = Point
                if  not self.IsValid():
                    self.top = Rect.top
                    self.bottom = Rect.bottom
                    self.left = Rect.left
                    self.right = Rect.right
                    return
                self.top = min(self.top, Rect.top)
                self.top = min(self.top, Rect.bottom)
                self.bottom = max( bottom, Rect.top )
                self.bottom = max( bottom, Rect.bottom )
                self.left = min( left, Rect.left )
                self.left = min( left, Rect.right )
                self.right = max( right, Rect.left )
                self.right = max( right, Rect.right )
            elif type(Point) == Area:
                Area = Point
                if isnan( Area.left ):
                    return
                if not self.IsValid():
                    self.top = Area.top
                    self.bottom = Area.bottom
                    self.left = Area.left
                    self.right = Area.right
                    self.Normalize()
                    return
                self.top = min( self.top, Area.top )
                self.top = min( self.top, Area.bottom )
                self.bottom = max( self.bottom, Area.top )
                self.bottom = max( self.bottom, Area.bottom )
                self.left = min( self.left, Area.left )
                self.left = min( self.left, Area.right )
                self.right = max( self.right, Area.left )
                self.right = max( self.right, Area.right )
                
            elif type(Point) == CFLine:
                Line = Point
                if not self.IsValid():
                    self.top = Line.m_Start.y
                    self.bottom = Line.m_End.y
                    self.left = Line.m_Start.x
                    self.right = Line.m_End.x
                    Normalize()
                    return
                self += Line.m_Start
                self += Line.m_End

if __name__ == '__main__':
    a = CFPoint(10, 5)
    b = CFPoint(10, 5)
    c = a+b
    d = CFCircle(c, 10.)
    print(a.x)
    e = CFLine(a, b)
    print(e.GetAngle())
    f = CFArc(a, 10, b, b, c)
    print(f)
    #print(c.x, c.y)
