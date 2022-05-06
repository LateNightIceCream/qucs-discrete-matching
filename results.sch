<Qucs Schematic 0.0.20>
<Properties>
  <View=-622,-140,1389,944,0.909091,349,0>
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
<Eqn Eqn1 1 50 410 -31 15 0 0 "S11_dB=dB(S[1,1])" 1 "yes" 0>
<GND * 5 320 250 0 0 0 0>
<GND * 5 240 270 0 0 0 0>
<GND * 5 420 300 0 0 0 0>
<GND * 5 210 300 0 0 0 0>
<.SP SP1 1 10 10 0 63 0 0 "lin" 1 "750 MHz" 1 "2 GHz" 1 "1000" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
<GND * 5 450 270 0 0 0 0>
<Pac P1 1 -90 270 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
<GND * 5 -90 300 0 0 0 0>
<GND * 5 100 250 0 0 0 0>
<SPICE TEMPLATE_6_0 1 100 220 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_5_0 1 210 270 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPICE TEMPLATE_4_0 1 320 220 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_3_0 1 420 270 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840110 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPfile X1_0 1 610 220 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
<GND * 5 610 680 0 0 0 0>
<Eqn Eqn2 1 50 760 -31 15 0 0 "S22_dB=dB(S[2,2])" 1 "yes" 0>
<GND * 5 320 600 0 0 0 0>
<GND * 5 240 620 0 0 0 0>
<GND * 5 420 650 0 0 0 0>
<GND * 5 210 650 0 0 0 0>
<GND * 5 450 620 0 0 0 0>
<Pac P2 1 -90 620 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
<GND * 5 -90 650 0 0 0 0>
<GND * 5 100 600 0 0 0 0>
<SPICE TEMPLATE_6_1 1 100 570 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_5_1 1 210 620 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPICE TEMPLATE_4_1 1 320 570 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_3_1 1 420 620 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840115 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPfile X1_1 1 610 570 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
<GND * 5 610 1030 0 0 0 0>
<Eqn Eqn3 1 50 1110 -31 15 0 0 "S33_dB=dB(S[3,3])" 1 "yes" 0>
<GND * 5 320 950 0 0 0 0>
<GND * 5 240 970 0 0 0 0>
<GND * 5 420 1000 0 0 0 0>
<GND * 5 210 1000 0 0 0 0>
<GND * 5 450 970 0 0 0 0>
<Pac P3 1 -90 970 18 -26 0 1 "3" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
<GND * 5 -90 1000 0 0 0 0>
<GND * 5 100 950 0 0 0 0>
<SPICE TEMPLATE_6_2 1 100 920 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_5_2 1 210 970 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPICE TEMPLATE_4_2 1 320 920 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_3_2 1 420 970 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPfile X1_2 1 610 920 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
<GND * 5 610 1380 0 0 0 0>
<Eqn Eqn4 1 50 1460 -31 15 0 0 "S44_dB=dB(S[4,4])" 1 "yes" 0>
<GND * 5 320 1300 0 0 0 0>
<GND * 5 240 1320 0 0 0 0>
<GND * 5 420 1350 0 0 0 0>
<GND * 5 210 1350 0 0 0 0>
<GND * 5 450 1320 0 0 0 0>
<Pac P4 1 -90 1320 18 -26 0 1 "4" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
<GND * 5 -90 1350 0 0 0 0>
<GND * 5 100 1300 0 0 0 0>
<SPICE TEMPLATE_6_3 1 100 1270 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_5_3 1 210 1320 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPICE TEMPLATE_4_3 1 320 1270 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_3_3 1 420 1320 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840118 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPfile X1_3 1 610 1270 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
<GND * 5 610 1730 0 0 0 0>
<Eqn Eqn5 1 50 1810 -31 15 0 0 "S55_dB=dB(S[5,5])" 1 "yes" 0>
<GND * 5 320 1650 0 0 0 0>
<GND * 5 240 1670 0 0 0 0>
<GND * 5 420 1700 0 0 0 0>
<GND * 5 210 1700 0 0 0 0>
<GND * 5 450 1670 0 0 0 0>
<Pac P5 1 -90 1670 18 -26 0 1 "5" 1 "50 Ohm" 1 "0 dBm" 0 "1 GHz" 0 "26.85" 0>
<GND * 5 -90 1700 0 0 0 0>
<GND * 5 100 1650 0 0 0 0>
<SPICE TEMPLATE_6_4 1 100 1620 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_5_4 1 210 1670 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPICE TEMPLATE_4_4 1 320 1620 -26 -112 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840027 (rev20a).s2p" 1 "_net1,_net2" 0 "yes" 0 "none" 0>
<SPfile TEMPLATE_3_4 1 420 1670 -812 -26 0 1 "/home/zamza/SharedFolder/qucs-discrete-matching/components/L/S-Parameter_7447840010 (rev20a).s2p" 1 "rectangular" 0 "linear" 0 "open" 0 "2" 0>
<SPfile X1_4 1 610 1620 -26 -59 0 0 "/home/zamza/SharedFolder/qucs-discrete-matching/antenna_data/aniou-antenna-large-raw-0R.s1p" 1 "rectangular" 0 "linear" 0 "open" 0 "1" 0>
</Components>
<Wires>
<350 220 420 220 "" 0 0 0 "">
<210 220 290 220 "" 0 0 0 "">
<420 220 580 220 "" 0 0 0 "">
<610 250 610 330 "" 0 0 0 "">
<210 220 210 240 "" 0 0 0 "">
<420 220 420 240 "" 0 0 0 "">
<130 220 210 220 "" 0 0 0 "">
<-90 220 70 220 "" 0 0 0 "">
<-90 220 -90 240 "" 0 0 0 "">
<350 570 420 570 "" 0 0 0 "">
<210 570 290 570 "" 0 0 0 "">
<420 570 580 570 "" 0 0 0 "">
<610 600 610 680 "" 0 0 0 "">
<210 570 210 590 "" 0 0 0 "">
<420 570 420 590 "" 0 0 0 "">
<130 570 210 570 "" 0 0 0 "">
<-90 570 70 570 "" 0 0 0 "">
<-90 570 -90 590 "" 0 0 0 "">
<350 920 420 920 "" 0 0 0 "">
<210 920 290 920 "" 0 0 0 "">
<420 920 580 920 "" 0 0 0 "">
<610 950 610 1030 "" 0 0 0 "">
<210 920 210 940 "" 0 0 0 "">
<420 920 420 940 "" 0 0 0 "">
<130 920 210 920 "" 0 0 0 "">
<-90 920 70 920 "" 0 0 0 "">
<-90 920 -90 940 "" 0 0 0 "">
<350 1270 420 1270 "" 0 0 0 "">
<210 1270 290 1270 "" 0 0 0 "">
<420 1270 580 1270 "" 0 0 0 "">
<610 1300 610 1380 "" 0 0 0 "">
<210 1270 210 1290 "" 0 0 0 "">
<420 1270 420 1290 "" 0 0 0 "">
<130 1270 210 1270 "" 0 0 0 "">
<-90 1270 70 1270 "" 0 0 0 "">
<-90 1270 -90 1290 "" 0 0 0 "">
<350 1620 420 1620 "" 0 0 0 "">
<210 1620 290 1620 "" 0 0 0 "">
<420 1620 580 1620 "" 0 0 0 "">
<610 1650 610 1730 "" 0 0 0 "">
<210 1620 210 1640 "" 0 0 0 "">
<420 1620 420 1640 "" 0 0 0 "">
<130 1620 210 1620 "" 0 0 0 "">
<-90 1620 70 1620 "" 0 0 0 "">
<-90 1620 -90 1640 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 850 682 444 322 3 #c0c0c0 1 00 1 0 0.2 1 1 -0.1 0.5 1.1 1 -0.1 0.5 1.1 315 0 225 "" "" "" "">
	<"S11_dB" #0000ff 0 3 0 0 0>
	  <Mkr 9.6021e+08 148 -401 3 0 0>
	  <Mkr 7.9004e+08 -76 -396 3 0 0>
	  <Mkr 1.70846e+09 435 -447 3 0 0>
	  <Mkr 1.87863e+09 468 -377 3 0 0>
  </Rect>
</Diagrams>
<Paintings>
  <Text 190 0 24 #000000 0 "Matching network template">
  <Text 190 40 12 #000000 0 "Using components:\nK1: /.../....s1p\nK2: /.../....sp\nK3: /.../....s1p">
</Paintings>
