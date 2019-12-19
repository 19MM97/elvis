PSCAD 4.2.1

Settings
 {
 Id = "1402001281.1404655503"
 Author = "Tamer Dallou.thefox"
 Desc = ""
 Arch = "windows"
 Options = 32
 Build = 18
 Warn = 1
 Check = 15
 Libs = ""
 Source = ""
 RunInfo = 
  {
  Fin = 1
  Step = 2e-006
  Plot = 2e-006
  Chat = 0.001
  Brch = 0.0005
  Lat = 100
  Options = 0
  Advanced = 4607
  Debug = 0
  StartFile = ""
  OFile = "noname.out"
  SFile = "noname.snp"
  SnapTime = 0.3
  Mruns = 10
  Mrunfile = 0
  StartType = 0
  PlotType = 0
  SnapType = 0
  MrunType = "mrun"
  }

 }

Definitions
 {
 Module("Untitled_1")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_2")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   0.import([126,126],0,0,-1)
    {
    Name = "Theta"
    }
   0.export([414,126],4,0,-1)
    {
    Name = "Ealpha"
    }
   0.import([234,162],0,0,-1)
    {
    Name = "Ed"
    }
   0.trig([198,126],0,0,-1)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([270,126],0,0,-1)
    {
    }
   0.import([126,216],0,0,-1)
    {
    Name = "Theta"
    }
   0.import([234,252],0,0,-1)
    {
    Name = "Eq"
    }
   0.trig([198,216],0,0,-1)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([270,216],0,0,-1)
    {
    }
   0.sumjct([342,126],0,0,-1)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "-1"
    G = "0"
    }
   -Wire-([342,162],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([306,216],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.import([126,324],0,0,-1)
    {
    Name = "Theta"
    }
   0.export([414,324],4,0,-1)
    {
    Name = "Ebeta"
    }
   0.import([234,360],0,0,-1)
    {
    Name = "Ed"
    }
   0.trig([198,324],0,0,-1)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([270,324],0,0,-1)
    {
    }
   0.import([126,414],0,0,-1)
    {
    Name = "Theta"
    }
   0.import([234,450],0,0,-1)
    {
    Name = "Eq"
    }
   0.trig([198,414],0,0,-1)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([270,414],0,0,-1)
    {
    }
   0.sumjct([342,324],0,0,-1)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([342,360],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([306,414],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   }
  }
 Module("Untitled_3")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_4")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   0.mult([648,72],0,0,990)
    {
    }
   0.datalabel([648,108],0,0,-1)
    {
    Name = "Van"
    }
   0.sumjct([738,72],0,0,1050)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "1"
    F = "-1"
    G = "0"
    }
   -Wire-([702,72],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([576,162],0,0,440)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([648,198],0,0,-1)
    {
    Name = "Vbn"
    }
   0.mult([648,162],0,0,990)
    {
    }
   -Wire-([684,162],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([576,234],0,0,440)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([648,270],0,0,-1)
    {
    Name = "Vcn"
    }
   0.mult([648,234],0,0,990)
    {
    }
   -Wire-([738,108],0,0,-1)
    {
    Vertex="0,0;0,126;-54,126"
    }
   0.datalabel([774,72],0,0,-1)
    {
    Name = "Vbeta"
    }
   0.const([576,72],0,0,450)
    {
    Name = ""
    Value = "0"
    }
   }
  }
 Module("Untitled_5")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_6")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_9")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_7")
  {
  Desc = ""
  FileDate = 1402333457
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_8")
  {
  Desc = ""
  FileDate = 1402333583
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_10")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   }
  }
 Module("Untitled_12")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   0.trig([216,234],0,0,50)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([288,234],0,0,60)
    {
    }
   0.trig([216,324],0,0,70)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.sumjct([360,234],0,0,100)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([360,270],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([324,324],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.trig([216,54],0,0,10)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([288,54],0,0,20)
    {
    }
   0.trig([216,144],0,0,30)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([288,144],0,0,40)
    {
    }
   0.sumjct([360,54],0,0,90)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([360,90],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([324,144],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([180,234],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([180,324],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([180,54],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([180,144],0,0,-1)
    {
    Name = "Theta"
    }
   0.mult([288,324],0,0,80)
    {
    }
   0.datalabel([396,234],0,0,-1)
    {
    Name = "Iq"
    }
   0.datalabel([396,54],0,0,-1)
    {
    Name = "Id"
    }
   0.pgb([396,54],0,52775776,120)
    {
    Name = "Vbeta"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([396,234],0,52776184,110)
    {
    Name = "Valpha"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([288,90],0,0,-1)
    {
    Name = "Ialpha"
    }
   0.datalabel([288,180],0,0,-1)
    {
    Name = "Ibeta"
    }
   0.datalabel([288,270],0,0,-1)
    {
    Name = "Ialpha"
    }
   0.datalabel([288,360],0,0,-1)
    {
    Name = "Ibeta"
    }
   }
  }
 Module("Untitled_11")
  {
  Desc = ""
  FileDate = 0
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-39,-39,39,39)
   Text(0,0,"$(Defn:Name)")
   }


  Page(A/A4,Landscape,16,[640,359],5)
   {
   0.mult([306,72],0,0,20)
    {
    }
   0.emtconst([234,72],0,0,10)
    {
    Name = ""
    Value = "14"
    }
   0.datalabel([306,108],0,0,-1)
    {
    Name = "Ia"
    }
   0.sumjct([396,72],0,0,140)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "-1"
    F = "-1"
    G = "0"
    }
   -Wire-([360,72],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([234,162],0,0,30)
    {
    Name = ""
    Value = "13"
    }
   0.datalabel([306,198],0,0,-1)
    {
    Name = "Ib"
    }
   0.mult([306,162],0,0,40)
    {
    }
   -Wire-([342,162],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([234,234],0,0,70)
    {
    Name = ""
    Value = "13"
    }
   0.datalabel([306,270],0,0,-1)
    {
    Name = "Ic"
    }
   0.mult([306,234],0,0,80)
    {
    }
   0.datalabel([432,72],0,0,-1)
    {
    Name = "Ialpha"
    }
   0.mult([540,180],0,0,60)
    {
    }
   0.datalabel([540,216],0,0,-1)
    {
    Name = "Ia"
    }
   0.sumjct([630,180],0,0,130)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "1"
    F = "-1"
    G = "0"
    }
   -Wire-([594,180],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([468,270],0,0,90)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([540,306],0,0,-1)
    {
    Name = "Ib"
    }
   0.mult([540,270],0,0,100)
    {
    }
   -Wire-([576,270],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([468,342],0,0,110)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([540,378],0,0,-1)
    {
    Name = "Ic"
    }
   0.mult([540,342],0,0,120)
    {
    }
   -Wire-([630,216],0,0,-1)
    {
    Vertex="0,0;0,126;-54,126"
    }
   0.datalabel([666,180],0,0,-1)
    {
    Name = "Ibeta"
    }
   0.const([468,180],0,0,50)
    {
    Name = ""
    Value = "0"
    }
   -Wire-([342,234],0,0,-1)
    {
    Vertex="0,0;54,0;54,-126"
    }
   }
  }
 Module("Main")
  {
  Desc = ""
  FileDate = 1404655272
  Nodes = 
   {
   }

  Graphics = 
   {
   Rectangle(-18,-18,18,18)
   }


  Page(C/A2,Landscape,21,[640,359],5)
   {
   0.voltmeter([378,36],0,0,10)
    {
    Name = "Vdcc"
    }
   -Wire-([378,72],0,0,-1)
    {
    Vertex="0,0;0,180"
    }
   0.peswitch([432,54],6,0,2040)
    {
    L = "D"
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([414,90],0,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([432,180],6,0,1980)
    {
    L = "D"
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([414,216],0,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([522,54],6,0,2030)
    {
    L = "D"
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([504,90],0,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([522,180],6,0,1970)
    {
    L = "D"
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([504,216],0,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([612,54],6,0,2020)
    {
    L = "D"
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([594,90],0,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([612,180],6,0,1950)
    {
    L = "D"
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([594,216],0,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   -Wire-([432,36],0,0,-1)
    {
    Vertex="0,0;0,18"
    }
   -Wire-([432,90],0,0,-1)
    {
    Vertex="0,0;0,90"
    }
   -Wire-([432,216],0,0,-1)
    {
    Vertex="0,0;0,36"
    }
   -Wire-([522,36],0,0,-1)
    {
    Vertex="0,0;0,18"
    }
   -Wire-([522,90],0,0,-1)
    {
    Vertex="0,0;0,90"
    }
   -Wire-([522,216],0,0,-1)
    {
    Vertex="0,0;0,36"
    }
   -Wire-([612,36],0,0,-1)
    {
    Vertex="0,0;0,18"
    }
   -Wire-([612,90],0,0,-1)
    {
    Vertex="0,0;0,90"
    }
   -Wire-([612,216],0,0,-1)
    {
    Vertex="0,0;0,36"
    }
   0.datalabel([468,90],0,0,-1)
    {
    Name = "g5"
    }
   0.datalabel([468,216],0,0,-1)
    {
    Name = "g2"
    }
   0.datalabel([558,90],0,0,-1)
    {
    Name = "g3"
    }
   0.datalabel([558,216],0,0,-1)
    {
    Name = "g6"
    }
   0.datalabel([648,90],0,0,-1)
    {
    Name = "g1"
    }
   0.datalabel([648,216],0,0,-1)
    {
    Name = "g4"
    }
   -Wire-([522,126],0,0,-1)
    {
    Vertex="0,0;198,0"
    }
   0.inductor([720,90],0,0,-1)
    {
    L = "0.9[mH]"
    }
   0.inductor([720,126],0,0,-1)
    {
    L = "0.9 [mH]"
    }
   0.inductor([720,162],0,0,-1)
    {
    L = "0.9 [mH]"
    }
   -Wire-([756,90],0,0,-1)
    {
    Vertex="0,0;126,0"
    }
   -Wire-([756,126],0,0,-1)
    {
    Vertex="0,0;126,0"
    }
   -Wire-([756,162],0,0,-1)
    {
    Vertex="0,0;126,0"
    }
   0.ammeter([882,90],0,0,30)
    {
    Name = "Ia"
    }
   0.ammeter([882,126],0,0,50)
    {
    Name = "Ib"
    }
   0.ammeter([882,162],0,0,80)
    {
    Name = "Ic"
    }
   0.capacitor([864,180],1,0,-1)
    {
    C = "250.0 [uF]"
    }
   0.capacitor([792,90],1,0,-1)
    {
    C = "250.0 [uF]"
    }
   0.capacitor([810,126],1,0,-1)
    {
    C = "250.0 [uF]"
    }
   -Wire-([918,90],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   -Wire-([918,126],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   -Wire-([918,162],0,0,-1)
    {
    Vertex="0,0;108,0"
    }
   0.voltmeter([972,90],0,0,40)
    {
    Name = "Vab"
    }
   0.voltmeter([990,126],0,0,60)
    {
    Name = "Vbc"
    }
   0.voltmeter([1008,144],2,0,70)
    {
    Name = "Vca"
    }
   -Wire-([1008,108],0,0,-1)
    {
    Vertex="0,0;0,-18"
    }
   -Wire-([1008,144],0,0,-1)
    {
    Vertex="0,0;0,18"
    }
   0.source_3([1170,126],4,0,-1)
    {
    Name = "Source 1"
    Type = "4"
    Grnd = "1"
    View = "0"
    Spec = "0"
    VCtrl = "0"
    FCtrl = "0"
    Vm = "0.381 [kV]"
    Tc = "0.05 [s]"
    f = "50[Hz]"
    Ph = "0 [deg]"
    Vbase = "230.0 [kV]"
    Sbase = "100.0 [MVA]"
    Vpu = "1.0 [pu]"
    PhT = "0.0 [deg]"
    Pinit = "0.0 [pu]"
    Qinit = "0.0 [pu]"
    R = "1.0 [ohm]"
    Rs = "1.0 [ohm]"
    Rp = "1.0 [ohm]"
    Lp = "0.1 [H]"
    R' = "1.0 [ohm]"
    L = "0.1 [H]"
    C = "1.0 [uF]"
    L' = "0.00005[H]"
    C' = "1.0 [uF]"
    IA = ""
    IB = ""
    IC = ""
    }
   0.resistor([1098,90],2,0,-1)
    {
    R = "0.0865 [ohm]"
    }
   0.resistor([1098,126],2,0,-1)
    {
    R = "0.0865 [ohm]"
    }
   0.resistor([1098,162],2,0,-1)
    {
    R = "0.0865 [ohm]"
    }
   0.hardlimit([126,954],0,0,1180)
    {
    UL = "400"
    LL = "-400"
    COM = "Hard_Limit"
    }
   0.sumjct([306,900],0,0,1290)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "-1"
    G = "0"
    }
   0.integral([270,612],0,0,1060)
    {
    Extrn = "0"
    Reset = "0"
    Mthd = "0"
    noname5 = ""
    INTR = "0"
    INTCLR = "0"
    T = "1 [s]"
    Yo = "0.0"
    YRst = "0.0"
    YHi = "100000000"
    YLo = "-100000000"
    }
   0.hardlimit([630,900],0,0,1400)
    {
    UL = "400"
    LL = "-400"
    COM = "Hard_Limit"
    }
   0.compar([54,306],0,0,1620)
    {
    Pulse = "0"
    INTR = "0"
    OPos = "1"
    ONone = "0"
    ONeg = "1"
    OHi = "1"
    OLo = "0"
    }
   0.inv([216,306],0,0,1660)
    {
    INTR = "0"
    }
   -Wire-([126,306],0,0,-1)
    {
    Vertex="0,0;90,0"
    }
   0.compar([54,378],0,0,1600)
    {
    Pulse = "0"
    INTR = "0"
    OPos = "1"
    ONone = "0"
    ONeg = "1"
    OHi = "1"
    OLo = "0"
    }
   0.inv([216,378],0,0,1650)
    {
    INTR = "0"
    }
   -Wire-([126,378],0,0,-1)
    {
    Vertex="0,0;90,0"
    }
   0.compar([54,450],0,0,1570)
    {
    Pulse = "0"
    INTR = "0"
    OPos = "1"
    ONone = "0"
    ONeg = "1"
    OHi = "1"
    OLo = "0"
    }
   0.inv([216,450],0,0,1640)
    {
    INTR = "0"
    }
   -Wire-([126,450],0,0,-1)
    {
    Vertex="0,0;90,0"
    }
   0.datalabel([324,306],0,0,-1)
    {
    Name = "g4"
    }
   0.datalabel([180,306],0,0,-1)
    {
    Name = "g1"
    }
   0.datalabel([162,378],0,0,-1)
    {
    Name = "g3"
    }
   0.datalabel([162,450],0,0,-1)
    {
    Name = "g5"
    }
   0.datalabel([324,450],0,0,-1)
    {
    Name = "g2"
    }
   0.datalabel([324,378],0,0,-1)
    {
    Name = "g6"
    }
   0.sig_gen([270,522],0,0,380)
    {
    Max = "1"
    Min = "-1"
    }
   0.mult([198,522],6,0,370)
    {
    }
   0.const([126,522],0,0,360)
    {
    Name = ""
    Value = "50.0"
    }
   0.const([162,486],0,0,340)
    {
    Name = ""
    Value = "100"
    }
   0.datalabel([324,522],0,0,-1)
    {
    Name = "Vtr"
    }
   0.pgb([342,522],0,53555064,390)
    {
    Name = "<Untitled>"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.sumjct([90,612],0,0,1040)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "-1"
    G = "0"
    }
   0.datalabel([54,612],0,0,-1)
    {
    Name = "Vq"
    }
   0.const([54,648],0,0,460)
    {
    Name = ""
    Value = "0.0"
    }
   0.gain([198,612],0,0,1050)
    {
    G = "1269.40"
    COM = "Gain"
    Dim = "1"
    }
   0.gain([198,666],0,0,1070)
    {
    G = "2.856"
    COM = "Gain"
    Dim = "1"
    }
   0.sumjct([342,612],0,0,1080)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([126,612],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([162,666],0,0,-1)
    {
    Vertex="0,0;0,-54"
    }
   0.integral([414,648],1,0,1830)
    {
    Extrn = "0"
    Reset = "0"
    Mthd = "0"
    noname5 = ""
    INTR = "0"
    INTCLR = "0"
    T = "0.001 [s]"
    Yo = "0.0"
    YRst = "0.0"
    YHi = "100000000"
    YLo = "-100000000"
    }
   0.sumjct([486,612],6,0,990)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([378,612],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.datalabel([414,684],0,0,-1)
    {
    Name = "Theta1"
    }
   0.mult([432,558],0,0,820)
    {
    }
   0.emtconst([360,558],0,0,410)
    {
    Name = ""
    Value = "1"
    }
   0.const([396,594],0,0,450)
    {
    Name = ""
    Value = "50.0"
    }
   0.integral([558,612],0,0,1000)
    {
    Extrn = "0"
    Reset = "0"
    Mthd = "0"
    noname5 = ""
    INTR = "0"
    INTCLR = "0"
    T = "1 [s]"
    Yo = "0.0"
    YRst = "0.0"
    YHi = "100000000"
    YLo = "-100000000"
    }
   0.datalabel([594,612],0,0,-1)
    {
    Name = "Theta"
    }
   0.pgb([594,612],0,53561184,1840)
    {
    Name = "<Untitled>"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.trans_filt([594,558],0,0,1540)
    {
    Order = "2"
    Band = "1"
    Type = "1"
    Cnfg = "0"
    FBase = "60.0 [Hz]"
    Flow = "10.0 [Hz]"
    Fup = "100.0 [Hz]"
    Q = "5"
    PRip = "0.1 [dB]"
    }
   0.div([666,558],6,0,1630)
    {
    }
   0.emtconst([702,522],2,0,400)
    {
    Name = ""
    Value = "1"
    }
   0.pgb([702,558],0,53603904,1850)
    {
    Name = "Frequancy"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([702,558],0,0,-1)
    {
    Name = "f"
    }
   0.datalabel([270,900],0,0,-1)
    {
    Name = "Iderf"
    }
   0.datalabel([306,936],0,0,-1)
    {
    Name = "Id"
    }
   0.gain([378,900],0,0,1310)
    {
    G = "64.57"
    COM = "Gain"
    Dim = "1"
    }
   0.pgb([684,900],0,53605944,1810)
    {
    Name = "Edcr"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([684,900],0,0,-1)
    {
    Name = "Edctr"
    }
   0.sumjct([306,990],0,0,1260)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "-1"
    G = "0"
    }
   0.datalabel([270,990],0,0,-1)
    {
    Name = "Iqerf"
    }
   0.datalabel([306,1026],0,0,-1)
    {
    Name = "Iq"
    }
   0.pgb([702,972],0,53607984,1770)
    {
    Name = "Eqctr"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([90,954],0,0,-1)
    {
    Name = "Vd"
    }
   0.datalabel([162,954],0,0,-1)
    {
    Name = "Vdlimit"
    }
   0.datalabel([1368,396],0,0,-1)
    {
    Name = "Qout"
    }
   0.datalabel([1368,432],0,0,-1)
    {
    Name = "Pout"
    }
   -Wire-([1368,396],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([1368,432],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   0.pgb([1386,396],0,53610024,1870)
    {
    Name = "Qout"
    Group = ""
    Display = "0"
    Scale = "1"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([1386,432],0,53610432,1860)
    {
    Name = "Pout"
    Group = ""
    Display = "0"
    Scale = "1"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.gain([1350,18],0,0,780)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,18],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,18],0,53611248,2010)
    {
    Name = "Van"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,18],0,0,-1)
    {
    Name = "Van"
    }
   0.datalabel([1314,18],0,0,-1)
    {
    Name = "Va"
    }
   0.gain([1350,54],0,0,790)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,54],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,54],0,53612880,1990)
    {
    Name = "Vbn"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,54],0,0,-1)
    {
    Name = "Vbn"
    }
   0.datalabel([1314,54],0,0,-1)
    {
    Name = "Vb"
    }
   0.gain([1350,90],0,0,800)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,90],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,90],0,53614512,1960)
    {
    Name = "Vcn"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,90],0,0,-1)
    {
    Name = "Vcn"
    }
   0.datalabel([1314,90],0,0,-1)
    {
    Name = "Vc"
    }
   0.gain([1350,144],0,0,120)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,144],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,144],0,53616144,130)
    {
    Name = "Vabn"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,144],0,0,-1)
    {
    Name = "Vabn"
    }
   0.datalabel([1314,144],0,0,-1)
    {
    Name = "Vab"
    }
   0.gain([1350,180],0,0,160)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,180],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,180],0,53617776,170)
    {
    Name = "Vbcn"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,180],0,0,-1)
    {
    Name = "Vbcn"
    }
   0.datalabel([1314,180],0,0,-1)
    {
    Name = "Vbc"
    }
   0.gain([1350,216],0,0,200)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,216],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,216],0,53619408,210)
    {
    Name = "Vcan"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,216],0,0,-1)
    {
    Name = "Vcan"
    }
   0.datalabel([1314,216],0,0,-1)
    {
    Name = "Vca"
    }
   0.gain([1350,270],0,0,230)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,270],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,270],0,53621040,250)
    {
    Name = "Ian"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,270],0,0,-1)
    {
    Name = "Ian"
    }
   0.datalabel([1314,270],0,0,-1)
    {
    Name = "Ia"
    }
   0.gain([1350,306],0,0,260)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,306],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,306],0,53622672,270)
    {
    Name = "Ibn"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,306],0,0,-1)
    {
    Name = "Ibn"
    }
   0.datalabel([1314,306],0,0,-1)
    {
    Name = "Ib"
    }
   0.gain([1350,342],0,0,310)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([1386,342],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.pgb([1458,342],0,53624304,330)
    {
    Name = "Icn"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1422,342],0,0,-1)
    {
    Name = "Icn"
    }
   0.datalabel([1314,342],0,0,-1)
    {
    Name = "Ic"
    }
   -Wire-([1026,90],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([1098,90],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([1134,126],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   -Wire-([1062,126],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   -Wire-([1026,162],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([1098,162],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([342,648],0,0,-1)
    {
    Vertex="0,0;0,18;-108,18"
    }
   0.datalabel([54,342],0,0,-1)
    {
    Name = "Vtr"
    }
   0.datalabel([54,414],0,0,-1)
    {
    Name = "Vtr"
    }
   0.datalabel([54,486],0,0,-1)
    {
    Name = "Vtr"
    }
   -Wire-([306,522],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.mult([846,432],0,0,810)
    {
    }
   0.emtconst([774,432],0,0,350)
    {
    Name = ""
    Value = "14"
    }
   0.datalabel([846,468],0,0,-1)
    {
    Name = "Van"
    }
   0.sumjct([936,432],0,0,950)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "-1"
    F = "-1"
    G = "0"
    }
   -Wire-([900,432],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([774,522],0,0,420)
    {
    Name = ""
    Value = "13"
    }
   0.datalabel([846,558],0,0,-1)
    {
    Name = "Vbn"
    }
   0.mult([846,522],0,0,830)
    {
    }
   -Wire-([882,522],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([774,594],0,0,470)
    {
    Name = ""
    Value = "13"
    }
   0.datalabel([846,630],0,0,-1)
    {
    Name = "Vcn"
    }
   0.mult([846,594],0,0,840)
    {
    }
   -Wire-([936,468],0,0,-1)
    {
    Vertex="0,0;0,126;-54,126"
    }
   0.datalabel([972,432],0,0,-1)
    {
    Name = "Valpha"
    }
   0.mult([846,666],0,0,870)
    {
    }
   0.datalabel([846,702],0,0,-1)
    {
    Name = "Van"
    }
   0.sumjct([936,666],0,0,960)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "1"
    F = "-1"
    G = "0"
    }
   -Wire-([900,666],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([774,756],0,0,570)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([846,792],0,0,-1)
    {
    Name = "Vbn"
    }
   0.mult([846,756],0,0,880)
    {
    }
   -Wire-([882,756],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([774,828],0,0,620)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([846,864],0,0,-1)
    {
    Name = "Vcn"
    }
   0.mult([846,828],0,0,890)
    {
    }
   -Wire-([936,702],0,0,-1)
    {
    Vertex="0,0;0,126;-54,126"
    }
   0.datalabel([972,666],0,0,-1)
    {
    Name = "Vbeta"
    }
   0.const([774,666],0,0,520)
    {
    Name = ""
    Value = "0"
    }
   0.trig([918,1080],0,0,1380)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([990,1080],0,0,1430)
    {
    }
   0.trig([918,1170],0,0,1410)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.sumjct([1062,1080],0,0,1480)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([1062,1116],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([1026,1170],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([882,1080],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([882,1170],0,0,-1)
    {
    Name = "Theta"
    }
   0.mult([990,1170],0,0,1470)
    {
    }
   0.datalabel([990,1116],0,0,-1)
    {
    Name = "Edctr"
    }
   0.pgb([1098,1080],0,53660536,1730)
    {
    Name = "Valpha"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1098,1080],0,0,-1)
    {
    Name = "Ectr_beta"
    }
   0.trig([630,1080],0,0,1340)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([702,1080],0,0,1390)
    {
    }
   0.trig([630,1170],0,0,1370)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.sumjct([774,1080],0,0,1440)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([774,1116],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([738,1170],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([594,1080],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([594,1170],0,0,-1)
    {
    Name = "Theta"
    }
   0.mult([702,1170],0,0,1420)
    {
    }
   0.datalabel([702,1116],0,0,-1)
    {
    Name = "Eqctr"
    }
   0.pgb([810,1080],0,53664616,1740)
    {
    Name = "Valpha"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([810,1080],0,0,-1)
    {
    Name = "Ectr_alpha"
    }
   0.datalabel([702,1206],0,0,-1)
    {
    Name = "Edctr"
    }
   0.trig([54,1080],0,0,970)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([126,1080],0,0,980)
    {
    }
   0.trig([54,1170],0,0,1010)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.sumjct([198,1080],0,0,1030)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([198,1116],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([162,1170],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([18,1080],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([18,1170],0,0,-1)
    {
    Name = "Theta"
    }
   0.mult([126,1170],0,0,1020)
    {
    }
   0.datalabel([234,1080],0,0,-1)
    {
    Name = "Vq"
    }
   0.pgb([234,1080],0,53669104,1760)
    {
    Name = "Vq"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([126,1116],0,0,-1)
    {
    Name = "Valpha"
    }
   0.datalabel([126,1206],0,0,-1)
    {
    Name = "Vbeta"
    }
   0.trig([360,1080],0,0,1090)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([432,1080],0,0,1110)
    {
    }
   0.trig([360,1170],0,0,1100)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([432,1170],0,0,1130)
    {
    }
   0.sumjct([504,1080],0,0,1140)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([504,1116],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([468,1170],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([324,1080],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([324,1170],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([540,1080],0,0,-1)
    {
    Name = "Vd"
    }
   0.pgb([540,1080],0,53673592,1750)
    {
    Name = "Vd"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([432,1116],0,0,-1)
    {
    Name = "Valpha"
    }
   0.datalabel([432,1206],0,0,-1)
    {
    Name = "Vbeta"
    }
   0.mult([450,270],0,0,1460)
    {
    }
   0.sumjct([558,288],0,0,1530)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "1"
    F = "0"
    G = "0"
    }
   0.mult([450,342],0,0,1520)
    {
    }
   0.datalabel([450,306],0,0,-1)
    {
    Name = "Ectr_alpha"
    }
   0.datalabel([450,378],0,0,-1)
    {
    Name = "Ectr_beta"
    }
   0.const([378,270],0,0,150)
    {
    Name = ""
    Value = "0.5"
    }
   0.datalabel([594,288],0,0,-1)
    {
    Name = "Ectr_b"
    }
   -Wire-([522,288],0,0,-1)
    {
    Vertex="0,0;0,-18;-36,-18"
    }
   -Wire-([522,324],0,0,-1)
    {
    Vertex="0,0;0,18;-36,18"
    }
   0.mult([450,414],0,0,1450)
    {
    }
   0.sumjct([558,432],0,0,1500)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "-1"
    F = "0"
    G = "0"
    }
   0.mult([450,486],0,0,1490)
    {
    }
   0.datalabel([450,450],0,0,-1)
    {
    Name = "Ectr_alpha"
    }
   0.datalabel([450,522],0,0,-1)
    {
    Name = "Ectr_beta"
    }
   0.const([378,414],0,0,280)
    {
    Name = ""
    Value = "0.5"
    }
   0.datalabel([594,432],0,0,-1)
    {
    Name = "Ectr_c"
    }
   -Wire-([522,432],0,0,-1)
    {
    Vertex="0,0;0,-18;-36,-18"
    }
   -Wire-([522,468],0,0,-1)
    {
    Vertex="0,0;0,18;-36,18"
    }
   0.mult([666,324],0,0,1510)
    {
    }
   0.sumjct([774,342],0,0,1590)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "1"
    F = "0"
    G = "0"
    }
   0.mult([666,396],0,0,1560)
    {
    }
   0.const([594,324],0,0,220)
    {
    Name = ""
    Value = "1"
    }
   0.const([594,396],0,0,290)
    {
    Name = ""
    Value = "0"
    }
   0.datalabel([666,360],0,0,-1)
    {
    Name = "Ectr_alpha"
    }
   0.datalabel([666,432],0,0,-1)
    {
    Name = "Ectr_beta"
    }
   0.datalabel([810,342],0,0,-1)
    {
    Name = "Ectr_a"
    }
   -Wire-([738,342],0,0,-1)
    {
    Vertex="0,0;0,-18;-36,-18"
    }
   -Wire-([738,378],0,0,-1)
    {
    Vertex="0,0;0,18;-36,18"
    }
   -Wire-([522,612],0,0,-1)
    {
    Vertex="0,0;0,-54;36,-54"
    }
   -Wire-([486,576],0,0,-1)
    {
    Vertex="0,0;0,-18;-18,-18"
    }
   0.datalabel([990,1206],0,0,-1)
    {
    Name = "Eqctr"
    }
   0.trig([756,918],0,0,1170)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([828,918],0,0,1230)
    {
    }
   0.trig([756,1008],0,0,1210)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([828,1008],0,0,1250)
    {
    }
   0.sumjct([900,918],0,0,1280)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([900,954],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([864,1008],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([720,918],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([720,1008],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([828,954],0,0,-1)
    {
    Name = "Ialpha"
    }
   0.datalabel([828,1044],0,0,-1)
    {
    Name = "Ibeta"
    }
   0.trig([1062,900],0,0,1120)
    {
    Type = "1"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.mult([1134,900],0,0,1160)
    {
    }
   0.trig([1062,990],0,0,1150)
    {
    Type = "2"
    Mode = "0"
    COM = "Trig-Func"
    Dim = "1"
    }
   0.sumjct([1206,900],0,0,1220)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([1206,936],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   -Wire-([1170,990],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   0.datalabel([1026,900],0,0,-1)
    {
    Name = "Theta"
    }
   0.datalabel([1026,990],0,0,-1)
    {
    Name = "Theta"
    }
   0.mult([1134,990],0,0,1200)
    {
    }
   0.datalabel([1242,900],0,0,-1)
    {
    Name = "Iq"
    }
   0.pgb([1242,900],0,53726496,1780)
    {
    Name = "Iq"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([1134,936],0,0,-1)
    {
    Name = "Ialpha"
    }
   0.datalabel([1134,1026],0,0,-1)
    {
    Name = "Ibeta"
    }
   0.datalabel([936,918],0,0,-1)
    {
    Name = "Id"
    }
   0.mult([594,666],0,0,510)
    {
    }
   0.datalabel([594,702],0,0,-1)
    {
    Name = "Ian"
    }
   0.sumjct([684,666],0,0,860)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "1"
    F = "-1"
    G = "0"
    }
   -Wire-([648,666],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([522,756],0,0,540)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([594,792],0,0,-1)
    {
    Name = "Ibn"
    }
   0.mult([594,756],0,0,560)
    {
    }
   -Wire-([630,756],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([522,828],0,0,600)
    {
    Name = ""
    Value = "12"
    }
   0.datalabel([594,864],0,0,-1)
    {
    Name = "Icn"
    }
   0.mult([594,828],0,0,610)
    {
    }
   -Wire-([684,702],0,0,-1)
    {
    Vertex="0,0;0,126;-54,126"
    }
   0.datalabel([720,666],0,0,-1)
    {
    Name = "Ibeta"
    }
   0.const([522,666],0,0,490)
    {
    Name = ""
    Value = "0"
    }
   0.mult([198,702],0,0,500)
    {
    }
   0.emtconst([126,702],0,0,480)
    {
    Name = ""
    Value = "14"
    }
   0.datalabel([198,738],0,0,-1)
    {
    Name = "Ian"
    }
   0.sumjct([288,702],0,0,850)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "-1"
    F = "-1"
    G = "0"
    }
   -Wire-([252,702],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.emtconst([126,792],0,0,530)
    {
    Name = ""
    Value = "13"
    }
   0.datalabel([198,828],0,0,-1)
    {
    Name = "Ibn"
    }
   0.mult([198,792],0,0,550)
    {
    }
   -Wire-([234,792],0,0,-1)
    {
    Vertex="0,0;0,-54;18,-54"
    }
   0.emtconst([72,828],0,0,580)
    {
    Name = ""
    Value = "13"
    }
   0.datalabel([144,864],0,0,-1)
    {
    Name = "Icn"
    }
   0.mult([144,828],0,0,590)
    {
    }
   0.datalabel([324,702],0,0,-1)
    {
    Name = "Ialpha"
    }
   -Wire-([234,864],0,0,-1)
    {
    Vertex="0,0;54,0;54,-126"
    }
   -Wire-([234,864],0,0,-1)
    {
    Vertex="0,0;-54,0;-54,-36"
    }
   -Wire-([720,162],0,0,-1)
    {
    Vertex="0,0;-288,0"
    }
   0.pgb([972,432],0,53737104,1880)
    {
    Name = "Valpha "
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([972,666],0,53737512,1820)
    {
    Name = "Vbeta "
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([54,306],0,0,-1)
    {
    Name = "Ectr_apu"
    }
   0.datalabel([54,378],0,0,-1)
    {
    Name = "Ectr_bpu"
    }
   0.datalabel([54,450],0,0,-1)
    {
    Name = "Ectr_cpu"
    }
   0.pgb([594,288],0,53739144,1930)
    {
    Name = "Ectrb"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([594,432],0,53739552,1890)
    {
    Name = "Ectrc"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([810,342],0,53739960,1910)
    {
    Name = "Ectra"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([936,918],0,53740368,1790)
    {
    Name = "Id"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.integral([450,900],0,0,1330)
    {
    Extrn = "0"
    Reset = "0"
    Mthd = "0"
    noname5 = ""
    INTR = "0"
    INTCLR = "0"
    T = "1 [s]"
    Yo = "0.0"
    YRst = "0.0"
    YHi = "500"
    YLo = "-500"
    }
   0.leadlag([522,900],0,0,1360)
    {
    Limit = "0"
    COM = "Lead_Lag"
    Reset = "0"
    YO = "0.0"
    G = "1.0"
    T1 = "4.835e-4[s]"
    T2 = "8.382e-6[s]"
    Max = "10.0"
    Min = "-10.0"
    }
   -Wire-([594,900],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   -Wire-([684,900],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.hardlimit([648,972],0,0,1350)
    {
    UL = "400"
    LL = "-400"
    COM = "Hard_Limit"
    }
   0.gain([396,972],0,0,1270)
    {
    G = "177.19"
    COM = "Gain"
    Dim = "1"
    }
   0.datalabel([702,972],0,0,-1)
    {
    Name = "Eqctr"
    }
   0.integral([468,972],0,0,1300)
    {
    Extrn = "0"
    Reset = "0"
    Mthd = "0"
    noname5 = ""
    INTR = "0"
    INTCLR = "0"
    T = "1 [s]"
    Yo = "0.0"
    YRst = "0.0"
    YHi = "500"
    YLo = "-500"
    }
   0.leadlag([540,972],0,0,1320)
    {
    Limit = "0"
    COM = "Lead_Lag"
    Reset = "0"
    YO = "0.0"
    G = "1.0"
    T1 = "2.376e-4[s][s]"
    T2 = "1.7058e-5[s]"
    Max = "10.0"
    Min = "-10.0"
    }
   -Wire-([612,972],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   -Wire-([702,972],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([342,990],0,0,-1)
    {
    Vertex="0,0;0,-18;18,-18"
    }
   0.inductor([144,72],0,0,-1)
    {
    L = "0.02 [H]"
    }
   0.capacitor([108,126],1,0,-1)
    {
    C = "470 [uF]"
    }
   0.capacitor([324,144],1,0,-1)
    {
    C = "4000[uF]"
    }
   0.peswitch([216,144],2,0,2000)
    {
    L = ""
    Type = "3"
    SNUB = "0"
    INTR = "0"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   0.peswitch([234,180],0,0,-1)
    {
    L = "T"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   -Wire-([234,144],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([234,180],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([612,252],0,0,-1)
    {
    Vertex="0,0;-288,0;-288,-72"
    }
   0.peswitch([252,72],1,0,-1)
    {
    L = "D"
    Type = "0"
    SNUB = "0"
    INTR = "1"
    RON = "0.01 [ohm]"
    ROFF = "1.0E6 [ohm]"
    EFVD = "0.0 [kV]"
    EBO = "1.0E5 [kV]"
    Erw = "1.0E5 [kV]"
    TEXT = "0.0 [us]"
    RD = "5000.0 [ohm]"
    CD = "0.05 [uF]"
    PFB = "0"
    I = ""
    It = ""
    V = ""
    Ton = ""
    Toff = ""
    Alpha = ""
    Gamma = ""
    }
   -Wire-([234,144],0,0,-1)
    {
    Vertex="0,0;0,-72;18,-72"
    }
   -Wire-([288,72],0,0,-1)
    {
    Vertex="0,0;0,-36;324,-36"
    }
   -Wire-([324,144],0,0,-1)
    {
    Vertex="0,0;0,-108"
    }
   -Wire-([324,252],0,0,-1)
    {
    Vertex="0,0;-36,0;-36,-36;-90,-36;-90,-72"
    }
   -Wire-([36,216],0,0,-1)
    {
    Vertex="0,0;-18,0;-18,-54"
    }
   -Wire-([18,126],0,0,-1)
    {
    Vertex="0,0;0,-54;126,-54"
    }
   -Wire-([180,72],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   -Wire-([108,162],0,0,-1)
    {
    Vertex="0,0;0,54"
    }
   0.datalabel([180,180],0,0,-1)
    {
    Name = "g_boost "
    }
   -Wire-([234,216],0,0,-1)
    {
    Vertex="0,0;-198,0"
    }
   0.voltmeter([54,144],0,0,20)
    {
    Name = "Vpv"
    }
   -Wire-([54,180],0,0,-1)
    {
    Vertex="0,0;0,36"
    }
   0.compar([234,1314],0,0,910)
    {
    Pulse = "0"
    INTR = "0"
    OPos = "1"
    ONone = "0"
    ONeg = "1"
    OHi = "1"
    OLo = "0"
    }
   0.sig_gen([126,1350],0,0,660)
    {
    Max = "1"
    Min = "0"
    }
   0.const([54,1350],0,0,640)
    {
    Name = ""
    Value = "5000"
    }
   -Wire-([162,1350],0,0,-1)
    {
    Vertex="0,0;72,0"
    }
   0.const([108,1260],0,0,630)
    {
    Name = ""
    Value = "0.25"
    }
   0.datalabel([324,1314],0,0,-1)
    {
    Name = "g_boost "
    }
   -Wire-([306,1314],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   0.div([180,1476],6,0,1190)
    {
    }
   0.const([108,1476],0,0,680)
    {
    Name = ""
    Value = "10000"
    }
   0.datalabel([180,1440],0,0,-1)
    {
    Name = "Vdlimit"
    }
   0.mult([252,1476],0,0,1240)
    {
    }
   0.emtconst([198,1530],0,0,740)
    {
    Name = ""
    Value = "14"
    }
   -Wire-([234,1530],0,0,-1)
    {
    Vertex="0,0;18,0;18,-18"
    }
   0.datalabel([288,1476],0,0,-1)
    {
    Name = "Iqerf"
    }
   0.sumjct([522,1476],0,0,710)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "-1"
    E = "0"
    F = "1"
    G = "0"
    }
   0.const([450,1476],0,0,700)
    {
    Name = ""
    Value = "816"
    }
   0.gain([1368,486],0,0,430)
    {
    G = "1000"
    COM = "Gain"
    Dim = "1"
    }
   0.datalabel([1332,486],0,0,-1)
    {
    Name = "Vdcc"
    }
   0.datalabel([1422,486],0,0,-1)
    {
    Name = "Vdccn"
    }
   -Wire-([1404,486],0,0,-1)
    {
    Vertex="0,0;54,0"
    }
   0.pgb([1458,486],0,53753424,440)
    {
    Name = "Vdcc"
    Group = ""
    Display = "0"
    Scale = "1"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.datalabel([522,1512],0,0,-1)
    {
    Name = "Vdccn"
    }
   0.gain([594,1476],0,0,720)
    {
    G = ".09"
    COM = "Gain"
    Dim = "1"
    }
   0.gain([594,1530],0,0,770)
    {
    G = ".6"
    COM = "Gain"
    Dim = "1"
    }
   -Wire-([558,1530],0,0,-1)
    {
    Vertex="0,0;0,-54"
    }
   0.sumjct([792,1476],0,0,940)
    {
    DPath = "1"
    A = "0"
    B = "0"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   0.integral([684,1476],0,0,730)
    {
    Extrn = "0"
    Reset = "0"
    Mthd = "1"
    noname5 = ""
    INTR = "0"
    INTCLR = "0"
    T = "1 [s]"
    Yo = "0.0"
    YRst = "0.0"
    YHi = "1000000"
    YLo = "-1000000"
    }
   -Wire-([648,1476],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([720,1476],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Wire-([792,1512],0,0,-1)
    {
    Vertex="0,0;0,18;-162,18"
    }
   0.datalabel([828,1476],0,0,-1)
    {
    Name = "Iderf"
    }
   -Plot-([1512,576],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [1512,576]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53737104,"Valpha ",0,,,)
     Curve(53737512,"Vbeta ",0,,,)
     }
    }
   0.pgb([324,1314],0,53756280,1720)
    {
    Name = "G_boost "
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   -Wire-([720,90],0,0,-1)
    {
    Vertex="0,0;-36,0;-36,18;-108,18"
    }
   -Wire-([612,90],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([594,54],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([504,90],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([504,54],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   -Wire-([432,90],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([432,54],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([612,216],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([612,180],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([522,216],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([522,180],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([432,216],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([414,180],0,0,-1)
    {
    Vertex="0,0;18,0"
    }
   0.ground([972,216],0,0,-1)
    {
    }
   -Plot-([1512,0],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [1512,0]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53611248,"Van",0,,,)
     Curve(53612880,"Vbn",0,,,)
     Curve(53614512,"Vcn",0,,,)
     }
    }
   0.voltmeter([918,162],0,0,90)
    {
    Name = "Vc"
    }
   0.voltmeter([936,180],0,0,100)
    {
    Name = "Vb"
    }
   0.voltmeter([954,180],0,0,110)
    {
    Name = "Va"
    }
   -Wire-([936,180],0,0,-1)
    {
    Vertex="0,0;0,-54"
    }
   -Wire-([954,180],0,0,-1)
    {
    Vertex="0,0;0,-90"
    }
   -Wire-([972,216],0,0,-1)
    {
    Vertex="0,0;-54,0;-54,-18"
    }
   0.mult([864,1242],0,0,900)
    {
    }
   0.mult([864,1314],0,0,920)
    {
    }
   0.mult([864,1386],0,0,1690)
    {
    }
   0.datalabel([864,1278],0,0,-1)
    {
    Name = "Van"
    }
   0.datalabel([864,1350],0,0,-1)
    {
    Name = "Vbn"
    }
   0.datalabel([864,1422],0,0,-1)
    {
    Name = "Vcn"
    }
   0.datalabel([828,1242],0,0,-1)
    {
    Name = "Ian"
    }
   0.datalabel([828,1314],0,0,-1)
    {
    Name = "Ibn"
    }
   0.datalabel([828,1386],0,0,-1)
    {
    Name = "Icn"
    }
   0.sumjct([1026,1314],0,0,1710)
    {
    DPath = "1"
    A = "0"
    B = "1"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([1026,1278],0,0,-1)
    {
    Vertex="0,0;0,-36;-126,-36"
    }
   -Wire-([954,1314],0,0,-1)
    {
    Vertex="0,0;-54,0"
    }
   -Wire-([900,1386],0,0,-1)
    {
    Vertex="0,0;126,0;126,-36"
    }
   0.datalabel([1062,1314],0,0,-1)
    {
    Name = "Pout"
    }
   -Wire-([990,1314],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   0.mult([1170,1242],0,0,650)
    {
    }
   0.mult([1170,1314],0,0,670)
    {
    }
   0.mult([1170,1386],0,0,690)
    {
    }
   0.datalabel([1170,1278],0,0,-1)
    {
    Name = "Vbcn"
    }
   0.datalabel([1170,1350],0,0,-1)
    {
    Name = "Vcan"
    }
   0.datalabel([1170,1422],0,0,-1)
    {
    Name = "Vabn"
    }
   0.datalabel([1134,1242],0,0,-1)
    {
    Name = "Ian"
    }
   0.datalabel([1134,1314],0,0,-1)
    {
    Name = "Ibn"
    }
   0.datalabel([1134,1386],0,0,-1)
    {
    Name = "Icn"
    }
   0.sumjct([1332,1314],0,0,930)
    {
    DPath = "1"
    A = "0"
    B = "1"
    C = "0"
    D = "1"
    E = "0"
    F = "1"
    G = "0"
    }
   -Wire-([1332,1278],0,0,-1)
    {
    Vertex="0,0;0,-36;-126,-36"
    }
   -Wire-([1260,1314],0,0,-1)
    {
    Vertex="0,0;-54,0"
    }
   -Wire-([1206,1386],0,0,-1)
    {
    Vertex="0,0;126,0;126,-36"
    }
   0.datalabel([1440,1314],0,0,-1)
    {
    Name = "Qout"
    }
   -Wire-([1296,1314],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   0.mult([1404,1314],0,0,1700)
    {
    }
   0.gain([1386,1422],0,0,760)
    {
    G = "1"
    COM = "Gain"
    Dim = "1"
    }
   0.emtconst([1314,1422],0,0,750)
    {
    Name = ""
    Value = "12"
    }
   0.pgb([828,1476],0,53868280,1670)
    {
    Name = "Idref"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.pgb([288,1476],0,53868688,1680)
    {
    Name = "Iqref"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   0.src_ccin_1([18,126],1,0,-1)
    {
    Name = "Source 1"
    Cntrl = "0"
    Vm = "0.05[kA]"
    f = "0[Hz]"
    Ph = "0.0 [deg]"
    Tc = "0.005 [s]"
    }
   -Wire-([864,216],0,0,-1)
    {
    Vertex="0,0;-18,0;-18,-126"
    }
   -Wire-([864,180],0,0,-1)
    {
    Vertex="0,0;0,-18"
    }
   -Wire-([1422,1422],0,0,-1)
    {
    Vertex="0,0;0,-72;-18,-72"
    }
   -Plot-([1512,1152],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [1512,1152]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53610024,"Qout",0,,,)
     Curve(53610432,"Pout",0,,,)
     }
    }
   0.datalabel([612,936],0,0,-1)
    {
    Name = "Icn"
    }
   -Plot-([1512,864],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [1512,864]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53740368,"Id",0,,,)
     Curve(53868280,"Idref",0,,,)
     }
    }
   0.pgb([162,954],0,53869912,1800)
    {
    Name = "Vq"
    Group = ""
    Display = "0"
    Scale = "1.0"
    Units = ""
    mrun = "0"
    Pol = "0"
    Min = "-2.0"
    Max = "2.0"
    }
   -Plot-([288,1224],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 0
    Area = [0,0,576,288]
    Posn = [288,1152]
    Icon = [288,1224]
    Extents = 0,0,288,18
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,288,90],"y")
     {
     Options = 0
     Units = ""
     Curve(53868688,"Iqref",0,,,)
     Curve(53868280,"Idref",0,,,)
     }
    }
   -Wire-([108,126],0,0,-1)
    {
    Vertex="0,0;0,-54"
    }
   -Wire-([54,144],0,0,-1)
    {
    Vertex="0,0;0,-72"
    }
   0.datalabel([180,1260],0,0,-1)
    {
    Name = "M_boost "
    }
   -Wire-([144,1260],0,0,-1)
    {
    Vertex="0,0;36,0"
    }
   -Plot-([1008,540],0)
    {
    Title = "Ectr"
    Draw = 0
    Area = [0,0,576,288]
    Posn = [702,144]
    Icon = [1008,540]
    Extents = 0,0,288,18
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,288,90],"y")
     {
     Options = 128
     Units = ""
     Curve(53993592,"a",0,,,)
     Curve(53994000,"b",0,,,)
     Curve(53994408,"c",0,,,)
     }
    }
   -Plot-([1188,342],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 0
    Area = [0,0,576,288]
    Posn = [1080,342]
    Icon = [1188,342]
    Extents = 0,0,288,18
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,288,90],"y")
     {
     Options = 128
     Units = ""
     Curve(53753424,"Vdcc",0,,,)
     }
    }
   -Wire-([864,360],0,0,-1)
    {
    Vertex="0,0;0,-36"
    }
   0.mult([936,396],6,0,1550)
    {
    }
   0.mult([936,342],6,0,1580)
    {
    }
   0.mult([936,270],6,0,1610)
    {
    }
   0.datalabel([900,396],0,0,-1)
    {
    Name = "scal"
    }
   0.datalabel([900,342],0,0,-1)
    {
    Name = "scal"
    }
   0.datalabel([900,270],0,0,-1)
    {
    Name = "scal"
    }
   0.datalabel([936,360],0,0,-1)
    {
    Name = "Ectr_c"
    }
   0.datalabel([936,306],0,0,-1)
    {
    Name = "Ectr_b"
    }
   0.datalabel([936,234],0,0,-1)
    {
    Name = "Ectr_a"
    }
   0.const([828,324],0,0,240)
    {
    Name = ""
    Value = "408"
    }
   0.const([792,396],0,0,300)
    {
    Name = ""
    Value = "1"
    }
   0.div([864,396],6,0,320)
    {
    }
   0.datalabel([972,270],0,0,-1)
    {
    Name = "Ectr_apu"
    }
   0.datalabel([972,342],0,0,-1)
    {
    Name = "Ectr_bpu"
    }
   0.datalabel([972,396],0,0,-1)
    {
    Name = "Ectr_cpu"
    }
   0.datalabel([216,1314],0,0,-1)
    {
    Name = "M_boost "
    }
   -Wire-([234,1314],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.delay([288,306],0,0,1940)
    {
    T = "0.000001[s]"
    INTR = "0"
    }
   0.delay([288,378],0,0,1920)
    {
    T = "0.000001[s]"
    INTR = "0"
    }
   0.delay([288,450],0,0,1900)
    {
    T = "0.000001[s]"
    INTR = "0"
    }
   -Plot-([324,1368],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 0
    Area = [0,0,576,288]
    Posn = [288,1152]
    Icon = [324,1368]
    Extents = 0,0,288,18
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,288,90],"y")
     {
     Options = 128
     Units = ""
     Curve(53756280,"G_boost ",0,,,)
     }
    }
   -Plot-([2088,0],0)
    {
    Title = "Frequncy "
    Draw = 1
    Area = [0,0,576,288]
    Posn = [2088,0]
    Icon = [2106,0]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53603904,"Frequancy",0,,,)
     }
    }
   -Plot-([2088,882],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [2088,882]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53726496,"Iq",0,,,)
     Curve(53868688,"Iqref",0,,,)
     }
    }
   0.emtconst([684,270],0,0,180)
    {
    Name = ""
    Value = "10"
    }
   0.div([756,270],6,0,190)
    {
    }
   0.const([720,234],0,0,140)
    {
    Name = ""
    Value = "2"
    }
   0.datalabel([810,270],0,0,-1)
    {
    Name = "sqrrt"
    }
   -Wire-([414,342],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   -Wire-([414,486],0,0,-1)
    {
    Vertex="0,0;-36,0"
    }
   -Wire-([810,270],0,0,-1)
    {
    Vertex="0,0;-18,0"
    }
   0.datalabel([414,342],0,0,-1)
    {
    Name = "sqrrt"
    }
   0.datalabel([378,486],0,0,-1)
    {
    Name = "sqrrt"
    }
   -Plot-([1512,288],0)
    {
    Title = "$(GROUP) : Graphs"
    Draw = 1
    Area = [0,0,0,0]
    Posn = [1512,288]
    Icon = [-1,-1]
    Extents = 0,0,576,288
    XLabel = " "
    AutoPan = "false,75"
    Graph([0,0],[0,0,576,225],"y")
     {
     Options = 128
     Units = ""
     Curve(53621040,"Ian",0,,,)
     Curve(53622672,"Ibn",0,,,)
     Curve(53624304,"Icn",0,,,)
     }
    }
   }
  }
 }

