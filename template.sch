<Qucs Schematic 0.0.20>
<Properties>
  <View=-20,-320,1500,944,0.909093,60,239>
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
  <.SP SP1 1 10 10 0 63 0 0 "lin" 1 "750 MHz" 1 "2 GHz" 1 "1000" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <SPfile X1 1 540 340 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 0 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
  <Pac P1 1 20 390 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND * 5 20 420 0 0 0 0>
  <GND * 5 540 420 0 0 0 0>
  <SPfile X2 1 540 160 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 0 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
  <GND *1 5 540 240 0 0 0 0>
  <Pac P2 1 250 210 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
  <GND *2 5 250 240 0 0 0 0>
  <Eqn Eqn1 1 640 340 -31 15 0 0 "S11_dB=dB(S[1,1])" 1 "yes" 0>
  <GND * 5 220 370 0 0 0 0>
  <SPICE TEMPLATE_4 1 220 340 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/C/CSRF_0402_885392005004_0R5pF.sp" 0 "_net1,_net2" 0 "yes" 0 "none" 0>
  <GND *5 5 310 440 0 0 0 0>
  <GND *6 5 340 410 0 0 0 0>
  <SPfile TEMPLATE_6 1 310 410 -118 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840012 (rev20a).s2p" 0 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
  <SPfile TEMPLATE_5 1 420 340 -157 30 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840012 (rev20a).s2p" 0 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
  <GND *3 5 420 370 0 0 0 3>
</Components>
<Wires>
  <540 370 540 420 "" 0 0 0 "">
  <540 190 540 240 "" 0 0 0 "">
  <250 160 250 180 "" 0 0 0 "">
  <250 160 510 160 "" 0 0 0 "">
  <20 340 20 360 "" 0 0 0 "">
  <20 340 190 340 "" 0 0 0 "">
  <450 340 510 340 "" 0 0 0 "">
  <250 340 310 340 "" 0 0 0 "">
  <310 340 390 340 "" 0 0 0 "">
  <310 340 310 380 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 860 472 444 322 3 #c0c0c0 1 00 1 7.5e+08 2e+08 2e+09 1 0.156404 0.2 1.07543 1 -1 0.5 1 315 0 225 "" "" "" "">
	<"S11_dB" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
  <Text 190 0 24 #000000 0 "Matching network template">
  <Text 190 40 12 #000000 0 "Using components:\nK1: /.../....s1p\nK2: /.../....sp\nK3: /.../....s1p">
</Paintings>
