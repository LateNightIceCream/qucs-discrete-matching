<Qucs Schematic 0.0.20>
<Properties>
  <View=-180,-120,1355,771,1,120,0>
  <Grid=10,10,1>
  <DataSet=template.dat>
  <DataDisplay=template.dpl>
  <OpenDisplay=1>
  <Script=template.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <.SP SP1 1 10 10 0 59 0 0 "lin" 1 "1 GHz" 1 "2.6 GHz" 1 "1000" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <R R1 1 210 270 15 -26 0 1 "50 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <R R2 1 420 270 15 -26 0 1 "50 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "european" 0>
  <GND * 5 210 330 0 0 0 0>
  <GND * 5 420 330 0 0 0 0>
<SPfile X1 1 610 220 -26 -59 0 0 "/home/zamza/Projects/qucs-discrete-matching/components/C/CSRF_0402_885392005012_4R7pF.sp" 1 "rectangular" 0 "linear" 0 "open" 0 "2">
  <GND * 5 610 330 0 0 0 0>
  <Pac P1 1 20 270 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 20 330 0 0 0 0>
  <Eqn Eqn1 1 50 410 -31 15 0 0 "S11_dB=dB(S[1,1])" 1 "yes" 0>
<SPfile X2 1 320 220 -26 -59 0 0 "/home/zamza/Projects/qucs-discrete-matching/components/C/CSRF_0402_885392005012_4R7pF.sp" 1 "rectangular" 0 "linear" 0 "open" 0 "2">
  <GND * 5 320 250 0 0 0 0>
</Components>
<Wires>
  <350 220 420 220 "" 0 0 0 "">
  <210 220 290 220 "" 0 0 0 "">
  <210 220 210 240 "" 0 0 0 "">
  <420 220 420 240 "" 0 0 0 "">
  <210 300 210 330 "" 0 0 0 "">
  <420 300 420 330 "" 0 0 0 "">
  <420 220 580 220 "" 0 0 0 "">
  <610 250 610 330 "" 0 0 0 "">
  <20 220 210 220 "" 0 0 0 "">
  <20 220 20 240 "" 0 0 0 "">
  <20 300 20 330 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 770 352 444 322 3 #c0c0c0 1 00 1 0 0.2 1 1 -0.1 0.5 1.1 1 -0.1 0.5 1.1 315 0 225 "" "" "" "">
	<"S11_dB" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
  <Text 190 0 24 #000000 0 "Matching network template">
  <Text 190 40 12 #000000 0 "Using components:\nK1: /.../....s1p\nK2: /.../....sp\nK3: /.../....s1p">
</Paintings>
