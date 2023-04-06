import c

def up(self):
    self.u2.upTrend=True
    self.u2.instanceShort=0
    self.u2.instanceLong+=1
    if self.u2.instanceLong==1:
        self.u2.newLong=True
        self.u2.shortClosed=None  

def down(self):
    self.u2.upTrend=False
    self.u2.instanceLong=0
    self.u2.instanceShort+=1
    if self.u2.instanceShort==1:
        self.u2.newShort=True
        self.u2.closed=None

def t(self, upmid, middown):
    if upmid>2 and middown>2:
        self.u2.strupTrend=True #
        self.u2.strdownTrend=False#
        up(self)
        
    elif upmid<-2 and middown<-2:
        self.u2.strdownTrend=True
        self.u2.strupTrend=False
        down(self)

    else:
        self.u2.strdownTrend=False
        self.u2.strupTrend=False

    if self.u2.upTrend:
        if c.kdjstrdownTrend and not self.u2.strupTrend:
            self.u2.newLong=False#
            down(self)
                
    elif not self.u2.upTrend:
        if c.kdjstrupTrend and not self.u2.strdownTrend:
            self.u2.newShort=False#
            up(self)
        #check whether elif is useful wait until tomorrow       
        elif c.kdjstrdownTrend and not self.u2.strupTrend and self.u2.instanceShort==0:
            self.u2.newLong=False
            down(self)
    
    c.upTrend=self.u2.upTrend
    c.strdownTrend=self.u2.strdownTrend
    c.strupTrend=self.u2.strupTrend
    c.instanceShort=self.u2.instanceShort
    c.instanceLong=self.u2.instanceLong
    c.closed=self.u2.closed
    c.shortClosed=self.u2.shortClosed
    c.newLong=self.u2.newLong
    c.newShort=self.u2.newShort