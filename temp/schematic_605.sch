<Qucs Schematic 0.0.19>
<Properties>
  <View=-572,-120,1231,771,1,552,0>
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
  <GND * 5 610 330 0 0 0 0>
  <Pac P1 1 20 270 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <Eqn Eqn1 1 50 410 -31 15 0 0 "S11_dB=dB(S[1,1])" 1 "yes" 0>
  <GND * 5 320 250 0 0 0 0>
  <GND * 5 240 270 0 0 0 0>
  <GND * 5 420 300 0 0 0 0>
  <GND * 5 210 300 0 0 0 0>
  <GND * 5 20 300 0 0 0 0>
<SPICE TEMPLATE_2 1 320 220 -26 -59 0 0 "C:\Users\rg\Desktop\qucs-discrete-matching\components\C\CSRF_0402_885392005001_0R3pF.sp" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_1 1 210 270 -766 -26 0 1 "C:\Users\rg\Desktop\qucs-discrete-matching\components\L\74279277.s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2">
  <SPfile X1 1 610 220 -26 -59 0 0 "C:/Users/rg/Desktop/qucs-discrete-matching/data/testdata.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
  <.SP SP1 1 10 10 0 63 0 0 "lin" 1 "750 MHz" 1 "2 GHz" 1 "1000" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
<SPICE TEMPLATE_3 1 420 270 -125 -26 0 1 "C:\Users\rg\Desktop\qucs-discrete-matching\components\C\CSRF_0402_885392005008_1R8pF.sp" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
  <GND * 1 450 270 0 0 0 0>
</Components>
<Wires>
  <350 220 420 220 "" 0 0 0 "">
  <210 220 290 220 "" 0 0 0 "">
  <210 220 210 240 "" 0 0 0 "">
  <420 220 420 240 "" 0 0 0 "">
  <420 220 580 220 "" 0 0 0 "">
  <610 250 610 330 "" 0 0 0 "">
  <20 220 210 220 "" 0 0 0 "">
  <20 220 20 240 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 760 572 444 322 3 #c0c0c0 1 00 1 0 0.2 1 1 -0.1 0.5 1.1 1 -0.1 0.5 1.1 315 0 225 "" "" "">
	<"S11_dB" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
  <Text 190 0 24 #000000 0 "Matching network template">
  <Text 190 40 12 #000000 0 "Using components:\nK1: /.../....s1p\nK2: /.../....sp\nK3: /.../....s1p">
</Paintings>
