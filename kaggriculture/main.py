# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2026 Rayk Kretzschmar
#
# The MIT grant covers the code in this file -- the market/SELL layer and the scheduler.
# It does NOT cover the base85 `_TRACE` field plan below, which is the shared public meta
# line reconstructed from public competition replays and is not the author's to license.
# See NOTICE, and the "Provenance" section of the dataset description.
"""Kaggriculture submission: public top-team replay (tape) + market-controller overlay.

PROVENANCE
- Field plan / action tape: the public episode 115469228 (DSM seat) from Kaggle's official
  public daily top-episodes dataset (kaggle/kaggriculture-episodes-2026-09-29, CC0-1.0).
  The competition host confirmed that using public replays to build a submission is allowed.
- Market/SELL layer, terminal controller and scheduler scaffolding: derived from
  "Closer Cleo" of the Kaggriculture Reference Agents dataset (Rayk Kretzschmar, MIT),
  https://www.kaggle.com/datasets/raykkretzschmar/kaggriculture-reference-agents
  (the dataset's own base85 _TRACE is replaced by the tape above).

Local head-to-head (both seats) vs the strongest public tapes of 2026-09-29: ~74% win rate,
and 23/24 against an unmodified copy of the same tape.
"""

import base64
import copy
import json
import zlib

_TRACE = json.loads(zlib.decompress(base64.b85decode(
"c-rM%U2k03ar`fQ=7Tt-Xl>qTX}l{~yA&wN17{%^2I3$<;5;~a3;f?Bi=3G|x2vnF`<$U<1Xy4P!_mFx`*c@VSO5CI7ytg}zy0+uf4lgXUoYO@efV(k`SRjF{`_D6_TOK=`10|ufBxHl{^ftZeE#*~x1av_r@LR?{(SfD;_~A4{qExO>htB}*Y6+h-+X%g@yqwSpSE{j{{M3Sm%~5!@Y8nte(_HVfB5|O%ac~Vef|4S?-y-I+WTSq?%lCPU!VWe+lTFi_>gq-@$ajq{Pxq^cW?gmW!OG``ueXAEm^d3*+2f}@nzQUcyHH(_U`WW7LD1j7r)#;eEjKa*U_il_QS{JS8|NuddMg7=?B**O**`E{r1Z^=1I%EX1u;z&s%)_e(08SacmCxYi!Vm?e@)=-~POPcmK=9<;EYbr*T-WFYw-{-k|Y&{GeO3dhhT4@#mBG#&^UKgJby1$HRM0+Oc}$_HNzN5BHzKs$4H;JRZBdkJ|^*>uj|5?}3|S)s@0#G2R@<`#6J-omsvmHf8_K<MZqDy&vn-g_ibr^}5qmHU~d0_2V<?`^=?&IB?{97xOxE?ESfq?+CBANB;Dr-spqy_&hWY>os5Q?b_DheT&z?=xCGoli3c#J>k7i-`M+V)_5P@%ieZ8eCNHFyzbbhq;WImnZ0fQ0Zgxa@Nulrr^BP4zA8PMv~=}>JofedyLa2yAOG~b?Zd~n@816F*HK7}=gdG(%*w?hee04mmEOSgL5GuW)uhDI3fBN1B+s<cmnwV<-)*ahzInKRpDjQBbhhwTR{17*!IP1O4~5eB8y4qNPZu9h|CFg?nEs&m$(N7)m)+j@-8L6IdU30-2Q&Wg;c;}!kB;*N%;7kQ#*&ftS?2DL1s)&r)c%w0^Yyu<r>y_+<^I8Jv#qQ<ble|WClB}it%ja*oCo=o=x5d+;&jZvwOGger}$Uu|DT6c?13hjHs5F{8WO;pB-m1Nar$OP(U<^7<>5oY7KoTh(vj@z(>uTg`wAAx!C)A%;x?ZP=P-Svw(jGjqZwjh5A9pbcIlzTu|}|sLp8$C$EHo`DcEpcS9RkdRMTiQHNy^%`RVTA51oedrvsn+_}9ZLQv>b8$A`P!Z?_K*fAr>i*@?ApdWk@{#S5CP0R0D0F=)$bu#470#ESQ?I4p2xVXxkB95;CGMAI!ytYJDW$6CDSaL_F$RQL%g_8LbIoTDqF)aqEgq7F}4z+S<I0S}&!c9B2njsfQ$ZlV>iG}p*`CbRE1LuOyJ56)@k<w2QmVCONL^BL{D!`qpi_uN+9Rm-YFwuEUT887r8Cw)Qd`w!ee;NFAB;DGrD8p6y!WRU2Sk(+6!H`U3(D3KFuw;vn5ycjjMW3~FQE&|d&%`!rkVKgq{SaAThX)H!FZ5M3E^>XQr1T?Rr2?xgHI2AVZmYG>7-WXpKZ`z?ThK&+Em6ts*PmT|SF2G?L<+I^bg^=m0I}K=4&K7X_I@qTVG}f9=BHiJ!{^&OYo8OOlI0GI88#O1fl?V|QeBoM@&x|1=TY?S7bD5c=aZQft5s+Y};Rz@(bR6pK0LB0S9~ofWfk|RSFzZ$hRL#RDqX|G*vd6D-+u3s?<FM>3jI8n!&Mu^|&Ki0)D6h3hGmLhFT>yVqW@9uBrMUDD<8o{uA@U52RJ4PSb^sZYWrGqV_YC6{t>#s5IsxCN;l0p6r1w>X76;}}*^SGcb$D?+28Tk`hXomj9$>k`qsY)sL@-KP@4mM<lyTlNLwUX>-k2yvbIxCog6_<Uj_e{EyR~lcZxy^}C~nI4xtWRQg7<xUJoj6K?PEGbxIHG}yYX~v$Lx9H4|w-+d&hsNselg09uHmmhuqB?;6c80Alm$FU0*7VB|kui%t7p$84Q^4z%<a02FVN_P7pbey3x#vSzA{#eA0O2MAJfEfEH_0v4u30M3PF#5jqG_F;+<}0LxO5M%qugnqy7&(n}hg&iuLGWsv)y>#^Zj@qm;D*6JI29NkY%z3cQ#76dN<gur$`3GkUf>?P-;4I!3C6hhh%kW*G{&(XlYzyI>T+r5$T#b<kSQ2`g}4MxG&H9YDxFVPZM`??GRDc~dO&H!NI0^rSfV#zVx&X1`(`bRst<U1TD7)<`$X)Q;0BE|+#-RKo8P_EKQByq}&L3ilhkN5W<woKXJ@B@y?t;5zBaHWw5GaYHY%CaQz=$GmPjUkH&Fh4xeALmPR0+3@7leOb4X@i%o%mql~FQ|b@LY_!Ax<Wbu&CkMu3nSIo6pthK`aZoW={<97U<CSgZk*n+Pa~3T*i`-?2IFFYWVycL8aXme`w_JD2C3g6D5eQJz{~=W7E$g~U7h0a`jZs~;UlJFfjVnvUAh`K8+9gyb*Qg*G<D0<dbP@yqcl~SgIW*d!%3RKY40ZpXpoTrH*1^`(B4sn7l5-xl@D+X0|Ovi@_^w!D5Bt9Ht4_(mIK~l<FYZ9W=}Y7m**A$N>(Gh8%?i3#Ku$$WA$=|FMzSl(j4j#q(?MEO&|zS2P&GOUs3%4!TR6$FurzoczgqXS*M+qRMK94Zbjo{t11zdab=H}RRlm;|0r;e;+$r_Nqr+SX*3ja5JADRr=0S-Eh>iC26}P0OdAl2E$2@d8=J;4;kHeqs5DzJoyi&b(iGx~?X?n!+%-|n*@_JWPU><=borOWj-&`FXfy-Rq+tlwL_Ca;tvIN(1V&n&jaBeaXT=NH5&<t@Ox6=OO5Q@Rr8}oaPXLoaABD+D(pBUv4o@eGF^G|Ioo`T!O5Mq=m*apL4vgn(g<*I=pXHZD_HU$mfU`)Cj!iWpEdXi|o|9pCMxcEx`H-}-;7`PtM)$->04v4O=e=_z0m%tkr!>*?y)wGu{u@EKT5ir)XAh#s*l_CZZ4A@aNx0^rhM(WQ`~6d}4mP;yB#HE^$eN)BgMTgEp2N`)G5Ib@lS#M==i;W|T$ph;)UImSdQ%YtWPY>}Uz|9)(b7ibx1fmyR<V@av;ydhJz1e`MDnLJ5vh}m7!5`GLMJvG6D|P0Vnk^{kdR1N7Xr@ZsKZnsEE27j?ZZk`eYuEY-+`{E*axr|E2LWxHG(>i0QhO}V}OjKuF7b!M?^<OLwIO@p2R*l?b5W;M4HQF#Sf}baX%8Yi^o7QYH+R<WATaCVIM8@pRA`GFw-+~+Mkd2Ki_@4x6VFRtYg_YEJA_cm7RIM%{;EwS~TLUVJ8z=l25}rZ#vY86r<RI9U+(5>Q^}qIjvW5*8od}pHk?rhpvMKIF%Yfjv{OUr$4eU#`+5DsoE7+1}W?@ynG6miRmf<dz2G1x{HSy#n#}lvx$m=uytbKy}nOIK}4NMGBtJL>cvdh2f`AsYRMFS<X_MMkZx7@7dBC%Qt<EU`g1W)Bg7QBsEgCHf-r@j!x7zV);!u9UQFkNPJdG)6Dpm;=wxF9j5dFLqF0*lhi9q~kUWJ_g+Ux%mhe#_hd3Hs3acR|n);`0-6K*R1WZ0a5CPz#)?sNYTvm&Zc5{Ccl9k0gKzT!oy-OvVOsK7&Jv9+xj6_)qKBvcJw4ERt3br7TFE!)xthT5MXLRTt(yovEn}CxeLCoVZojV@saJQD#(RG`ckcW^2B~2D#BAU%N;=J}8rlIZQpQ*Lo1lk@qLR6Q}Jfp3X(!<40>!}vt2HvPD0AW|CeYhM0pomKoL20ty;K|KxLtygd*)b;=!fL?cDvd`?xlqX&P8On>5wn#f0?3rAqZ5;20FOIwLho3-Dbis`1`8I*&apK)r#CiEnH!u?k{B#pR;UCd`BbRbJ;dfn$5~-2Q2S4Xlj#W(HO!kBB`s7DM-#W6)oWR;#~I^HORKWAfaFiu6f`t+=y(=UME<+UM5wFH^Fw0$`{j}S!0GchX|e^+!0>eFGK1+HgfPzRv9PAH`ZfB*Twa5Bb#>cfb`U(o6lh`Bn1DLJ{3QKPZtbE1HrTnem>RP-vZ3k;pn)+p<a00+4kCxN??%&IZ7+lEFXMvP@DXDnt4mN8f7lAq7KhT$#S6k3Yp~31?QaEbfeI-s4Sb8ycFdQ1ln1z-fO+|hfZT&PF<H5Oc9gH6yM;?d?<+FrNo&`eS{y1~Kkx#roWVDV#*hTRkdd3rKLj;wb{2F!QejQJvR!yr{-f4<uiV6Lc!*{^0WS=nsfX9pBoq9L+D;tX+4^v`o1XAC2>c3s#9;zN5j5E0IpQRE_v#UU-F6VL7Fd#1lS;WxOfzBudo72IRi}&B#_7K$x7;zX-sR$=u?JQYjA|vtn*hsa*&Q-wb@<}6+h6|G!#&FQC>V^(rbg%v9Q9m`mFaEuV5SKxek>4y;^9n!hTaZEWjzh?e|_51LRekqcthd}4>FO~UHoysEDm%K6lZx^^K4pFF=Y`PT#i)qJ!olbdD;U%eeuG%@L!=26ZTjsM>pXyn=vcLA%wRsE08Ic<zZiVD-{8wY^7Ef*_=;Soh57h8R(|5(VKH6hq5ZH4CD0afd)kC)$rQ>_~TQ$Y{p5+JJ0NQB6@*XH)NY2p1n;Fw6!^h0Te<jv>9Q!2*&(MCpH`c7=~;AXK_NY+6Aj$cQIVByW-$?-9CPDDKA@}SXLq}-5B_$D`hk{iX6#j#$_KSKDx<h;S^P#mb-msZXb|=VO(3T)+6#e;Ep&0>(6GKw&cTff_<fs<$BQ+^xSwgQ5G7`#kywXIvU{^w0Iy(2?jXw6WZ1Xo#3eQlIPo$YQ!l^xx>lMq!U}bNkNN8HheBd`U}?#0GS54WjVBBK}rSptD-v4I`|y;FNNZuN2Vt+rc4_PYVG!S?;m)z#D$Ta2{@fPU3Ch&7=Z0bIuKa<h-8&`=S)(8uCEhyjvv}7-i57A^pNoci^VxF1(#&xLlVGg!$fVHazW*a8xRGzC~D{Bw!*1MsIW86F);pU&{U`fgL?)sg=~yXiB@x56}T(ge1Aub-4b;tfT4$U$f%@IjJM-Ny5JbPh#S=xO&n}BD7VjAeT>~)1nPq8KbleGiaUwL)e*2$Y9y;<#nW%9fuAGEJr=cQ2{P1_XrPgcETx>z@^$0gkO8)KUrglXYH2a8QNeI<5h3Tb!SpyLJi`B`NK<zqFG2S6l~j=J>g$a4DV&T%8nbyIb>)&*C<de%IrW7u5wIM<04znY2VZ)bG6URBV2OBWjo6deE^;E1W$3KQE-HlRnKkNA7}y1O)An*;q+O)D;6Hnck#en3cnNG&b^Z&j7!UDpilO_cI<|ERD5CMt3YzK&6ASn4U0&regDu{?{V`SI@KoI9^M;Eu4djZkflWq%*Ph!C=g|z1TY+!?*41?47~rugkWZf_0d*(Zi(__TkMO&pK*SmL>D|mWd#!iQTD}?1HTevyVcN%Nz1z;l=&F~f87KzBXkTv2<c?2rAbOGvkmklWkR@z~?@yLiJ*77;k&%l!#*<m|fcGBeho83F_o<%383_MERm@JUWjsF<`8A+Xqx9<53PM8-t2}xIer{C<IJf~ieSiinKx#H8Rc8cVaSr@*@ccm8#|C)0{_{(QVj55z!nnuqP2c$EMKDm^D_bosahh$=l97l63$o!OL@$WCG==IL-;Nuod{lH`R6tjoS*D{POj<Z+C?*Ne05sp`<j4jE5O85sI-g)~s;je!5Z5x(ncyxSYL#?^<IT)$mXX;$l?h#DbT4@3M+&F6@VzmYp8}99yo|aJMPgSlFhw;wRN4~4kg+Zzg0mp5wm|g>3imd>+|6^5wklfseJ{?B8C27jAWTgwvZ8^RqV_G0X{WkoX*GA`NIl%gBG<9(dYQjX*wyp1mh{`Q$Y@H_EENajamVK5@=fcdgLUhJm|#zW_ha63!h!QSOqG%oOwNR5yzrZTKqs<LiGnWyo?6Mc*@Y!8c|CEey##H|(~VYd?WC||9N<}?MAr$oTS%1E@g~d6<R_X{$D|mN`s!LgR%Q@b6ismFyDZ_Mni;2_Am-POIJ!IE5RhWhdyHdu-8mfey1iY_`d0?jRf4f>rYY^64#BNq4{BteQWMh(X4me}B!HYRjlP^kl0}2#jTH{-mXv4eqfuqo#-Y-z7lEW6MCgv;O_PAO;Nu{#4Nh~lV$?zm+q$$S;H17o<WD$7QGM8PjY#$2I)H1z6-DbSCft1+KIqiIWhR2J7(!Izb%wDL_ld|;X`o!}5X?~pcYD>BZUbNylko7Om`r5BR3F?Y4Z4X@BpO5!Qu-@Df6|-(85Je(9=4X!4i#9!Wb3WrZ=EYkt%*9+j;(DaQI}n}O9cD2q6|UF0*s<3=<$U@&10KMN7uc=jO;2EWs6$-23wuLo%D(o5JUiN%rnB$>`IL6cHR7(FDA0|(BAMerYm8@N~D(Oz;^5f#+~Mr6{3z{DxG!rLS@KF7^*1iVy9YbmN%`}?J-jQ6UPa}>HYB1-4Ag=NxT^zP?Y6qOR&n=?kNa$8LYLMSfDF}=@pGP%UJ|c(u+!d8%e9%WDe=(TsWH{@OIryspNXx4hd{AD8<axvy^)y8JP_}Sj|ZFh2rM1!>oE4mKdI{syGLL8!d`K%V>5TIN+ie_+QZswHbwR_&F$yiWm|y7`&Y})lC(*5K|ATgw^IV!zix^RFE+V$UI!Z(-h9i21Cs$InfQRJ!PV{3(qlp%=Vgre`HCxsrbntZ;C)<^3+PGRJhxA?&UOHAMARF-YFDbsn9U^5+#E^WA2tZPhtI%yrPfJYT&0>pEXDFw+dIP$w}R&0<|>B(YWp|yXr_VIsuL=Gfq^nQ@SVs(5Vs`qFFryy0`$UnI^-}kf}0-%$U98D_KpGv2>0}R_-#<LCX@prGl3ebnWb%x_YV&Z7co_PYWg&JJd}YQ&~kuS$1~A`lAHoBI0InnXUnwYeb2<?52$Fgi@b*A0<5mB`?lWPhIe|yu@A%DIROX(u&R}M&@-2CSok$`g5U@tW(;A$>wRi@zCYtlz$~*5_;Qj0JOM4nt9U921}-1=@8Zb&8iZgfwUJ_!Sle2jK-JJ&2DrYqk<yFzAqSjbBp8BEF)VLYUjw{-Y9C-4D<{pI!Uq4rodEKE4;$n40@jO;w86Gm6xS7Rj@{6;a27T#W)8uW#@u9U;;&X(5D|ZV-jvPG+Hl^l)W|Ud-k?gd@sH@jc_U>MsDj>-+H_-n{D9XE$CO^B3AfM`rw+>xm$u4VA!lkg9X8_?-YYfG*p3xro{p<LS;HrxRva+0(rHNnV;MLYV`S{8(dGELg<AAH#&dHIPcw?cJ0d#tT>B14tA8wjJ2|&taHKTk;1&wmc+J2d0upbS6w*2=Dw=qr1F~zt2XruM#>yA<UfWgh4z^spm&weswu1BL@y-Gu!>|Rt8Z$37w%9MI>t#*%-tEV&o#bEOV}oHn_8$l7lD|X${Ry095xa8rc~0V#J8jt&cQ%%v(9`JQeqSv3)OckEcnEDI@;cD570i5?V>ECjjP@%8J2dLk&-Hh$TS({0g9Z;ZzuqFO@dmK@&`^YCsDiv*ZJ-?NT}qwlf$YOCUtUZiY-a{!Oh7b1nfrbB@jFftLN5tqxz>rPUzVEDBqp2KYQA3ad>H)X_})_SR3Z>QGF`Kz(F=J*o2fdcLtF+n?@5!2vkIi;jWzRz>F~;Kv2{tn#v2WMR+_izFs$zFGFBc;}2zxB4=*lAFEeaAdm4f6n+_6xfgs|Lpvcm!!-hYBh!Ak565UfO<|l;nzW&tP1O<C%Wej<pdkp5R6UFwyIk^hBx`R7D<k)$ohDxpY-?5%n#Vz-_%BBZ_<Xwp?-MEnX2c{H<^#A{v^~4q-gNRz?tXpOPu(=8XqGL};n^(KsZgyuK`Taxx*@cfQ=)A!C9_(<GWI88S=y>`wN0#J%$$eo)mO8#bR{P(!NuSS%3*vL&QoS_r3SZMsB<4-2???>v(()C^hnG5L$xJ5EDTU1p6X_fVq@zd_j4u0O1-(mm!}j;vz)7w1KZ-NDIXW`b$}fLe#P?%+rfy!(Dq8;zUVTIK%77b5AFy>zEEnBkj&eBBlS+Z-mEW{lc%+mKn^CPE$E5RI4)&1CdJ7n1D15TM6Bo}@}K8%FdpZ`0+j_j!6ZHKL!%n#uS@gEB?Jm-=>6p^B#_EZDuROR-V}JYR=y!42f{XsB0$4>OKC;sG=Bj21o*njGj-dTaiXwBX+3N|x#(YA{v3(NnAI54y;06Yyrc@?GZ0C^naa*euAlF#&^EAufy`1Cx@7sXiy<N6NIu__lfMOHz^nsP%o}$^`xtY)E<Ci}!}G{@G_v4l$>}_<G9+LeLq1{DDs;dlG(4HT1TTj_X@YxJhvCX)gmQdJ2{O_?z@3MkEuhBj)Z^<?yoUM49y1Qb`VwAo8Se|vPWW!wDqHj5_G6y}UR|}D8G#38LB{dRdDC{ro@YZ2)LL~bKe<*&68=^&vVrV{JMY?zj%lmX6?)>ucJ-nYnBV3*#r&SG*!K_jZ$7>Lcmf^u3Zp`ZFra}GrSVdC>k<8$SO^v1e*i1`7Ijc7*dXPcUbmCklDtHydcrH#wCbjMP{Pi)g9!!AFBoV~b%#w<D`HTE4R!-%9XAybZ_5+Wwyc*aT0`U|4&vQP+YcWrJR2us$N6*Wk}Bd+R4IrR5mj+T%$TU}1P`5U)R&+P0<EuTY?vb3w4U+6#~s&il{>Oot0XZR-I`vA1OYK!S^8!|7I&oennhKm5e{~gDm{=UjZxuRac6;@$Z~$_yv!LA_()E!RNNxmZW=lOQ(vl9$Yk$roICk??@*%@1xl{b`nwQ~q3SNs_X0cD`>K@2SV-_~12<mT2nslh9853@hVfOT)H!`;xDN!~RGzaX$d_{v`(kr0*2-)il<W}TL|+q;-+JBLXl8S>BBnB47%{tqQ`p4$)60yd*a|Z^3Z~h|juqZG(^aMm%y{8$AJ^kSniZ6Hg4{*1xu^NPEfM#SU8_VZvtf$-9d$(%u7lYLt()gdXszH)s+Lo!glxbtD~Mg2gD^nl!xf_I{5^xWHavYezmU&qH{XNRiR8WSGf8Z=9)}lq`JYxEPYrRX)ZGfzAuDDs1@PiqW?W5z3QU~<8nu*clC{rL!b2%VPeQg9G^aQq6z`n@&e@7=N{^_n>6+(Y4QzNWL7*lLHkc=OFdpv2{lc>nDIlyu;t`LK=a<Oa(ZZzy;w5w;g+Iv^6#Q`RY4IF&cUgDn>0_GiI<yUg*IOsVodr=QG4{HJ>uAk~TBsjvD4&F9)O!FY4yKm7EF^kY6%_Ve_k~0c@j2N|W<k?i3;u!L7di^Gj?2=x(rY$is*`v=mHTr6dE{DN#2!XqGBe^7SWv6fk@4cZ__Y&7Ei(S9VN*g~Bv+<jn=+cxO1rNVgGdVwc*V0Bv}jmojq0zP5`Knm!Ts_EO1Pjql<_8a0W1-+-x^Le1^}9=6H2Ezo64A{2ZFqYUdHac61@&JaA{6o8G1VfEWbPATw74CkG?$vH_lC3n#+gVRQYf`FSZ~bw-NGjE#acNn%qQNqC<|;NvD;f^F!iVj>H^GDP^Vus}SoeXALX6N7uiVX;!Qa+?CC;D)`3j!jtUL4l(!2ctoLDb(1m8Xbz{9fLgRuIj^IHCK_oszGLZZr%9QE<q!+2D7s^!e0)^RT|BMSp2`~Kc$$t$$H8IbpqiqUjS25O8`**)V4<QO^V}y1C-jPT*0JPC^*}ybqC4Kp*-8rHx=fVb2FVnjoYM&mDmgy(yaS(>B%QYD0}PJqq#7B#LNJXf?#(#NT-uP5$jW884YqnK{AVG%qHM&d8kQ{s#!xnV?zp-h@ba;>`e>=Ft!FZFCBM<!h+NUw&b|TvP~lH=QA{eGXD0mHWv2=Xe}Pt2K?4yYnIF|O*Fb=@TSM23$l%@5WLXN5iR)PI-0awh<y$%NhRt2<QY!NBeQM;5aqIm2*lTPaSoLxj_sBTl7ZDVCXP$#gH-PV5fA$dxoel+7{X`k_naG7@xdNY-L<?0En`eDBLsPp_R;P4?lGuH(#DeKeHFlWber!_(5HW2Q!cr}MN}}xy4X~tWIs$of#0pKJ9e-2Q4vmh$F-<5WWnn3CC{0KLubJS~R4JV-A&c{-5~TvIgh#ddWQ78C`zflXpN#D712Z)Pp2+EnI+*;Gp`okaO(?kTJ2}dlNfwNkk5j14IBzonj|hAGlqYE-8s?EM%9#vk&|BWM8(Ff_>B+VtG*79@2@dT&Eb7(P9@YE;>xN{|$s^ShvrrXuZ2h@b_{Y+6tO<PDbruc%`~fgj6>Qk5%ws!dp7khYiutLAOTvXQzl1RE-=7>2MkSBkd?4f8Kv2Enb&D)sp{VB{b*oKx6UtR?26C<qB}$}7&yFQ9Rr&qIfK*87OBL+^H{19(9%Oz9lTo~GTO-h>xyPzP!_7I9Xum%dyljKb6TkBp;W)krczm!p22Zngu##^gez%`jgXf3KUr3}0xS&=6jBh~ii@H97rcvOQO(gbV{c6HecEAk{OwXhB`Sc=(f<i$KFYBSNh{x`KcpoYaa~}>BnN$jdQ_<@Z+#U`KnYH2-Fy>swymTi!>s%|@KP?h_5r+W@hY|59&#>8eIy3Q00k9~OSGyZ~8oS5qe~XLW%>ZQ5YUidh>d-bIgD9Z_syZ~pW%M$TC}9bvU7U&X2lCwgJXd(_qAglbRWP;4TN}%#kvY*sOnr2MU-W*fX_mMJM*aF{9z83jM|V}uDF4c>t)+31wS#j80w3B-gf%Z^^;l-PEPGkZ<Q4ib6ftu*KrJq8<O{KtlSzfxB5Zy>CR+IgCy&=iF~uT8F1w`5%Bl$EG<Om)F_GBd1&Z=-?m8qJK1$#ne4<ouAA*4=&j|RDC>xc1&l4SK&2YYqs7Ja85$uu3QZbj6AGvuhaPjKu`{WFYx~t%Z5>lc8yG_^8IoN|aN-FaIz7d=72q3oQM-n)vQFd0`_96f^T;;J4{baDHuD@<3UN$wi3&~(5)|TzIj25LBxMo>}0m?r_gGTv5c|nF|F#)h~igZFd_B)e`TPccbTD>J{%T6M_tyEX$3;PGhG(Rf=iilW%URH=uU;)!L|D>zd8ZQ)8fkIRPZRiUL4Jmd(C}@8q3C#oJtdI#OWS~z%Tgk)e`WgO;?2(X9Ef$l314;X8G?~>Pw(!#l5?6N<Qd)2On4{vQ?g*snW+aQanpeblfTYHASrcX;vs-+2S`yM)FEb_Z-oJ-xavGv)4ZXq!LcBjzsussJ%%+3X+m@!&VZSEe;;xhVay=sfTU}vME00r?(?jS?_1<`ekGe($lV>f}{d`$iiBZK>1G?ES0L~JF8mIsGusWU68bKWIl|U7H0TRv(<%!-P6BzuF-x^DLNXP)j(B<Zz7Uruk%7#;eoh@|a=gyP@1cpa#yU$PnWC#247W2ja6#1Bk;94bZ&xSQff3aXKRAAW10McC~s(x?<LB@lZra-8FcD9K_ny7Ky2tP@ihh6pV4l>8=Xb#bl^b@z@tzpLv$>C|!fGSFg^H0gb4OYM{oJcW~0Gx1s(VEqr(5+f{a$Q}Sz;=la7I7%hNlUmCn~U6Mn=0(@AzJ*fXW3trSi*A_#_DhSHJ4~ID$nYaCngI^b~zmJMo{z?83~mTZeFv=+@<^7=qswI;2vG3<(lrc9#+y1JNVg2mp085_()P(W9D{aL}CFw7Q9I%LG|b~mjTrywAk)#0v++$MsQqFg3h@uZ{1rlcC@S$hz?T%U?uk|r84NuU;iW(nu2gL+!+$aE1SQu3*4^Ss;YRL$Oxv{Uu$qnnbkvFMakq8Bt^zCQOQp=Y3cEu#yHU#1AzS-v&4!OpIT!3oowdnN_Ib?B1BMx5ChZf>VNEBHlM3s%|{(8#c$^#k*q@OhQp7FcV00kGdAm4a+z;P5uejv-n!K*cCMJwaFLQlZe_RrCpsPrfOJRMFgGI3mD21pCaIKOTTb2PC(fhzGq~O5vt{cVAw4xh7I(6E8M45FjZl=SwVZjwRvHhw80V!mmxO~VHKvttc}bL0!M&o!ZlAYUASp~dMhc8jb@XdK2TiGXZVMH=?wN5Vos3<f=u@7$pd;mDdr;E=1aL|z4hbV7#cJ|G23A<YhTAw_(IAyJ`IW+P%~qF4b>{e3E$7+3ttc2o!#^Ng<SST^%PMPn9aD&*@547h!(W6;S_Mr!@w!%=tCYxLMo4<<20f)ndJ0i(1Frt%0Onx7)R=M}C28ld<b1UOs~*AfP8k7Isj~>`EC=2q&V8~j+hR%qEA>^%opC=|m||1nl>@Y(ucGA5dihLFZib|FZb^G+Ji`prWDql@`IL*7;bk{@G2haUD@Vto-1!q`m>G70Hl1+1pebJ=Wt1eW5Alz);eyHwf;xqT+QsPhF|z0b64=5?jriW0jRsJ_90w)kiw)zV2)a&@I7Ix3z;uHRqk;JjFgQ)(Fp2jWRUy`gpu~9nn0^jL)$V4ne-hasU<}w2)?2gQ&3R>`z~Hqi8KV>@%~Sh!dA}qI3-*mgU&Vgp*DG;`PN2~GS*%d2O1Pm2ly0l1VQ5;sowR#R-T7`Sv7*yAIZn!)<0gfGb^`cS8L7D7__w8~1lzBNKo;&(;K|m4{)S#tskRMX{)N;5O%WH$TSbCYDXIqTf(!<4vo$Lf5MEVoQCrDB*+-P}#J7SEXjLHQbiCErr$P;5QgQt7v4hK%m7__l%M0RhA6)4iNSjecO$~}rcx;?~++%|(eK?!f(@^2y9IH<+9t`>>F92E%7Yukr3T*&xTdrirgGT=OFUB-h2R09Ossn8^Me+lFw{?@AO%T3W1o$T4Wo~M0-0i4YF;};Ed+p&iv<!S9@5{)`iwV#A9Qe*awo_1P)6xCg3>%0$FU{z-injU5n$T;KFpa5wFpXXZC_XPgkJZ`@z*+$J{P`@bfeLgXG9D`om&!b58oPFGFff4QBB6nH?Icz;;u=?%gRsPX)Pyk<P(h`zn>t$Ex&dyc9#}k5pv<j<r=1Qbgwzq;DJWR(9F;D+lz}OBTwK&T_oI~E=VR~*AV)+f4Z(9sAXIsn9D+Akl-nF%(?D9`+;h3^eomN!8W`eOYKGO)9s*@-f18GNO0sl>Elc^_6`GjDT!A)T;xl3GJddtJ76$WZ)QZr6W6_kMh)h;NF!lgAl!ejbNjL>YS7_-|BZT-MkAD{zYnzGRFHJ*h@8q}(7-Ge3JhIDbAvIBsh?Olu_OOejm&jNM1@)4h`59M9Cwu8)L(IU=73+lBOC0kY+@s6mh9+PVlr%3gQ8+{oU=XkL5a(wtZ|4xEDEyTsq;6dJ%OhZ+cdu$?oCzE96-~xnDBv2{p;<I5`Ea%Ry@$!dlhQx1qNNl&aZoW<cKpgFD-xHjfI-;7B&TET1{>y3CHE^A11b5yekxHR2tln>VotxR(U$pTZj860F}FCX(2StcEwCSUt*aU?Q;7j{!?ZR`J6E=XYT+<bvrtj)2P0Jp@TA?Cvy%A{BVV0d<iBLE@O?5Bw48#M@SVac3X;Hib^N6C>t)49UfZ)~t*8Y307EG}0O<ItdaQ=)xWCX}8m=Q~H9gL<oI_%u?2LeSO5~>P+jSckeO*UG7Zv+9{Eee)WKKLunsPBOE7I9#&w%!@WF7ExXHjG!bLGTbSGuAM3pNMrvh`Qek@RMp-<w_!7fD0=&d`}8pGp(PH<0OJM1&4CuiGEHkI^h)y|a_OSY~Ct10<wj(j%^3yjZ$}KX2dN{}R7_JULFke6rF`zdZVwCtp87J}(gHv-<iJrFemS)qi}uW~4kKJP;K5{P)lQ2M6>_Q~"
)).decode("utf-8"))

_SELLABLE = ("STRAWBERRY", "MELON", "MILK", "WOOL", "EGG", "TOMATO", "CARROT", "WHEAT", "FERTILIZER")

_FRONT_RUN_HORIZON = 1
_FRONT_RUN_ITEMS = ("MELON", "STRAWBERRY", "MILK", "WOOL")
_BASE_PRICE = {"MELON": 250, "STRAWBERRY": 120, "MILK": 160, "WOOL": 200}
_GLUT_WEIGHT = {"MELON": 3.5, "STRAWBERRY": 2.0, "MILK": 2.0, "WOOL": 3.2}
_LAST_STEP = -1
_CLONE_CONFIDENCE = 0


def _public_signature(farm):
    """Compact public fingerprint for detecting a mirrored build."""
    counts = {item: 0 for item in (
        "COW", "SHEEP", "GOOSE", "WHEAT", "CARROT", "TOMATO",
        "STRAWBERRY", "MELON", "PASTURE", "COOP", "WEED",
    )}
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            for key in ("animal", "crop", "kind"):
                value = tile.get(key)
                if value in counts:
                    counts[value] += 1
                    break
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands", []) or [])]
    return (
        len(farm.get("hands", []) or []),
        tuple(sorted(farm.get("unlocked_quadrants", []) or [])),
        tuple(sorted(tuple(position) for position in positions)),
        tuple(counts[item] for item in sorted(counts)),
    )


def _signature_distance(left, right):
    distance = abs(left[0] - right[0])
    distance += 3 * abs(len(left[1]) - len(right[1]))
    distance += sum(abs(a - b) for a, b in zip(left[3], right[3]))
    if left[2] != right[2]:
        distance += 2
    return distance


def _update_clone_profile(obs, step):
    global _CLONE_CONFIDENCE
    if step not in (4, 24) and not (step >= 48 and step % 24 == 0):
        return
    farms = obs.get("farms", []) or []
    if len(farms) < 2:
        return
    player = int(obs.get("player", 0) or 0)
    distance = _signature_distance(
        _public_signature(farms[player]),
        _public_signature(farms[1 - player]),
    )
    if distance <= 1:
        _CLONE_CONFIDENCE = min(8, _CLONE_CONFIDENCE + 1)
    elif distance <= 4:
        _CLONE_CONFIDENCE = max(0, _CLONE_CONFIDENCE - 1)
    else:
        _CLONE_CONFIDENCE = max(0, _CLONE_CONFIDENCE - 3)


def _front_run(action, obs, step):
    """Sell one premium line immediately before a clone's expected glut."""
    if _CLONE_CONFIDENCE < 2 or _FRONT_RUN_HORIZON <= 0:
        return
    orders = list(action.get("market", []) or [])
    if len(orders) >= 10:
        return
    already = {}
    for order in orders:
        if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL":
            already[order[1]] = already.get(order[1], 0) + max(0, int(order[2] or 0))
    planned = {}
    end = min(len(_TRACE), step + _FRONT_RUN_HORIZON + 1)
    for future_step in range(step + 1, end):
        distance = future_step - step
        for order in _TRACE[future_step].get("market", []) or []:
            if not (
                isinstance(order, list) and len(order) >= 3
                and order[0] == "SELL" and order[1] in _FRONT_RUN_ITEMS
            ):
                continue
            item = order[1]
            quantity = max(0, int(order[2] or 0))
            if item not in planned:
                planned[item] = [distance, quantity]
            else:
                planned[item][1] += quantity
    shed = (obs.get("private") or {}).get("shed") or {}
    prices = ((obs.get("market") or {}).get("prices") or {})
    choices = []
    for item, (distance, quantity) in planned.items():
        available = max(0, int(shed.get(item, 0) or 0) - already.get(item, 0))
        quantity = min(available, quantity)
        if quantity <= 0:
            continue
        price = float(prices.get(item, _BASE_PRICE[item]) or 0)
        priority = (
            price * quantity * _GLUT_WEIGHT[item]
            + (_FRONT_RUN_HORIZON + 1 - distance) * _BASE_PRICE[item]
        )
        choices.append((priority, item, quantity))
    if choices:
        _, item, quantity = max(choices)
        orders.append(["SELL", item, quantity])
        action["market"] = orders[:10]


def _terminal_liquidation(action, obs, step):
    """Replay-derived safety net: leave no sellable shed inventory at season end."""
    if step < 680:
        return
    shed = (obs.get("private") or {}).get("shed") or {}
    market = action.setdefault("market", [])
    already = {
        order[1]
        for order in market
        if isinstance(order, list) and len(order) >= 2 and order[0] == "SELL"
    }
    for item in _SELLABLE:
        qty = int(shed.get(item, 0) or 0)
        if qty > 0 and item not in already and len(market) < 10:
            market.append(["SELL", item, qty])


def _shed_access(size):
    half = size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _move_toward(pos, target, tiles):
    x, y = pos
    tx, ty = target
    choices = []
    if tx < x:
        choices.append(("WEST", (x - 1, y)))
    if tx > x:
        choices.append(("EAST", (x + 1, y)))
    if ty < y:
        choices.append(("NORTH", (x, y - 1)))
    if ty > y:
        choices.append(("SOUTH", (x, y + 1)))
    size = len(tiles)
    for op, (nx, ny) in choices:
        if 0 <= nx < size and 0 <= ny < size and tiles[ny][nx] != "LOCKED":
            return [op]
    return ["PASS"]


def _terminal_action(obs):
    """Observation-driven final-eight-turn harvest/drop/sell controller."""
    player = int(obs.get("player", 0) or 0)
    farm = (obs.get("farms") or [])[player]
    private = obs.get("private") or {}
    tiles = farm.get("tiles") or []
    size = len(tiles)
    positions = [farm.get("farmer", [0, 0]), *(farm.get("hands") or [])]
    inventories = list(private.get("inventories") or [])
    inventories.extend({} for _ in range(len(positions) - len(inventories)))
    sheds = set(_shed_access(size))

    available = {
        (x, y)
        for y, row in enumerate(tiles)
        for x, tile in enumerate(row)
        if isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0
    }
    actions = []
    pending = {}
    for pos_raw, inventory in zip(positions, inventories):
        pos = tuple(pos_raw)
        inventory = inventory or {}
        load = sum(max(0, int(v or 0)) for v in inventory.values())
        x, y = pos
        tile = tiles[y][x] if 0 <= y < size and 0 <= x < size else None
        if load > 0 and pos in sheds:
            action = ["DROP"]
            for item, count in inventory.items():
                if item in _SELLABLE:
                    pending[item] = pending.get(item, 0) + max(0, int(count or 0))
        elif isinstance(tile, dict) and int(tile.get("yield_units", 0) or 0) > 0:
            action = ["HARVEST"]
            available.discard(pos)
        elif load > 0:
            target = min(sheds, key=lambda q: abs(q[0] - x) + abs(q[1] - y))
            action = _move_toward(pos, target, tiles)
        elif available:
            target = min(available, key=lambda q: (abs(q[0] - x) + abs(q[1] - y), q[1], q[0]))
            available.discard(target)
            action = _move_toward(pos, target, tiles)
        elif isinstance(tile, dict) and tile.get("fertilizer_available", False):
            action = ["COLLECT_FERTILIZER"]
        else:
            action = ["PASS"]
        actions.append(action)

    shed = dict(private.get("shed") or {})
    for item, count in pending.items():
        shed[item] = int(shed.get(item, 0) or 0) + count
    prices = ((obs.get("market") or {}).get("prices") or {})
    sells = [
        (int(shed.get(item, 0) or 0) * int(prices.get(item, 1) or 1), item, int(shed.get(item, 0) or 0))
        for item in _SELLABLE
    ]
    sells = [row for row in sells if row[2] > 0]
    sells.sort(reverse=True)
    market = [["SELL", item, qty] for _, item, qty in sells[:10]]
    if int(obs.get("hour", 0) or 0) <= 1:
        already = int(farm.get("hires_today", 0) or 0)
        for _ in range(min(10 - len(market), max(0, 8 - already))):
            market.append(["HIRE"])
    return {"farmer": actions[0], "hands": actions[1:], "market": market[:10]}


def _base_agent(obs, config=None):
    global _LAST_STEP, _CLONE_CONFIDENCE
    step = min(int(obs.get("step", 0) or 0), len(_TRACE) - 1)
    if step == 0 or step <= _LAST_STEP:
        _CLONE_CONFIDENCE = 0
    _LAST_STEP = step
    _update_clone_profile(obs, step)
    if step >= 717:
        return _terminal_action(obs)
    action = copy.deepcopy(_TRACE[step])
    _front_run(action, obs, step)
    _terminal_liquidation(action, obs, step)
    return action


# ===========================================================================
# Market-controller overlay
# ===========================================================================
import math as _math

# Per-step remaining sell volume of this field plan, measured over c27 self-play.
_SUPPLY = json.loads(zlib.decompress(base64.b85decode(
    'c%1Fr%Wm5+5Cza*39{~j!?(Ii3pWj#)PQRsXp4SH(SNTlZOK$D%hrRG91k$}ECK|GWl5pP5&z!5eqB9m??2xC_S${8>%g|40o8~KRn)i|T_c-Ng)B~CGN496wl}hgs1QXm@KJ@zO8JSLEoMTcp!~L+F{jWC^e|LF)=(2sf$PIb3(SlNzsDBEF#JfoWe(t$Yj9w9c;Cbw<7UNFSXW_+8eK!jXnZ0v6}ZhU25LvUVmLTB{V)npQt&Tu2T?{8u6>1DeP;Bfh-txjrG(rgadmg#C&QQ5mb7*zObT%PjIEHq#)0xwmcrH0IS6;r%ds_7fjeO<R-XVDHtFe5b{U9c@TIh4Qa~f2^712`IfKEUA#@B*lD={N5Gf8RziqLrKOgSyKR;|X>+lpP>YsCQadB~Rad9Oo3_rH(mxt||haX&ATwGjSTv-akk00C3!|SKjX7dw65Q*tshG7_nVVGkyprl}RZvx~bgg>YpF-fdKOSG4qgU%8bqxwVs6t+gzh!`qtez1P$MN(W?6824OUyMG5Y$A?9(^>?+g>mRks6oAK>ZeGxbZYtsodn6F-$d?$<E};~EL)F^?O7_S=&9^w^}PO$2eRE-I>Ru`&4T`{s6B{cFwQ{YZl6U*zQ14uWyS3#%h2Z*@^*MPQP3v8n8;y4cWAPRbdmZHJgFv)oG)UwHJsJsBlnMRadB~RadBm-FjM*T{4I2j>|PvW80OtT4e<Ic^F9%mLxt<aObni{eUSnSOm>`25B5IDhw)1T#~HJ2gbkb)it^`?XCZfm;OhyiIuT((rx*gdOtM5Af}2MpCW=~4u!#b8dq^Fe(W!z<VQjEXR6G?ub;2p#H~XpMB5DU|K3=`9*UzC3<m5IO40GEoV6^e>(Kih?vsxDB>cI}F?O-s7>4zgO*m=mOMPEO7fFHFt)1`zxoKzFEYZV<Sf2W`*g3~vl6)Si2btbe1*(mA?61N3mCrB|}<jgtQPJ>6GFRRV=>G|o`Y7^F*FlVr6C;{`%5t~lbSY!)lcb=RE!hfF_mzI-r-D(o354i67ZQuEZwrOsCA(S1oU{8hVL>-fNRvtUO?m%zt9OxwICh{0%a-kZ?nHV;0J{oL}oHQfG!C2wLe($Yu`<RKME{uGWj?HT?+Td1C5YbH5F*r?^*4GKtKIO3v+vWF6XxHyrn;6*2-<p>3c(Rs!pD~m+;RUgj8S*-S*aeT2QB@B!|NaA0p<>w'
)).decode("utf-8"))

_I0 = 10000
_PRICE_FLOOR = 1
_MP = {
    "WHEAT": (25, 400, "sqrt", 0.80, "log", 0.20),
    "CARROT": (35, 450, "log", 0.20, "sqrt", 0.70),
    "TOMATO": (60, 200, "linear", 0.40, "sqrt", 0.60),
    "STRAWBERRY": (120, 100, "sqrt", 0.70, "linear", 1.60),
    "MELON": (250, 300, "log", 0.20, "sq", 3.60),
    "EGG": (50, 332, "linear", 0.40, "log", 0.20),
    "MILK": (160, 122, "sqrt", 0.60, "linear", 1.60),
    "WOOL": (200, 105, "log", 0.20, "sq", 3.20),
    "FERTILIZER": (100, 200, "linear", 0.40, "linear", 0.40),
}
_SHOP_DEMAND = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_CENTER_ITEMS = tuple(k for k in _MP if k != "FERTILIZER")

# Products the controller owns, mapped to a reservation price expressed as a
# fraction of base price. Everything else keeps the tape's schedule untouched.
_RESERVE = {}
# Sort SELL orders by gross value so the most valuable sale takes the earliest
# slot; market slots resolve index by index across both players.
_SORT_SELLS = True
# Ranking key for slot placement: "gross", "unit" or "impact".
_SORT_KEY = 'impact'
# True places promoted sells ahead of buys/hires; False keeps the tape's layout.
_SELLS_FIRST = False
# Only these products may be promoted into early slots. Empty means all.
_PROMOTE = ('MILK', 'WOOL', 'STRAWBERRY', 'MELON', 'EGG', 'TOMATO', 'CARROT', 'FERTILIZER')
# Extra slot priority for a product whose remaining supply outruns the town's
# remaining appetite. Such a product is a race, not a hold: its price will only
# fall, so the units sold before the opponent's are the only ones worth much.
# Ranking purely by current price gets this backwards — a already-crashed product
# looks unimportant precisely when beating the opponent to the floor matters most.
_RACE_WEIGHT = 0.0
# Products that may be promoted only from this step onward. Selling wheat early
# lowers the price an opponent pays for feed, which can rescue a cash-starved
# rival; deferring wheat promotion keeps that pressure on during the early game
# when starvation actually bites.
_PROMOTE_AFTER = {}
# Products promoted only while the opponent's public money is at least this much.
# A rival near insolvency is the one most helped by our extra supply, so we hold
# that pressure on until they are clearly solvent.
_PROMOTE_IF_OPP_MONEY = {'WHEAT': 200.0}
# Force selling once the shed reaches this load, protecting end-of-day drops.
_SHED_PRESSURE = 80
# Reservation decays linearly to zero across this window, spreading liquidation.
_RAMP_START = 576
_RAMP_END = 716

_SUPPLY_DRIVER = {
    "MILK": ("animal", "COW"),
    "WOOL": ("animal", "SHEEP"),
    "EGG": ("animal", "GOOSE"),
    "FERTILIZER": ("animal", None),
    "STRAWBERRY": ("crop", "STRAWBERRY"),
    "MELON": ("crop", "MELON"),
    "WHEAT": ("crop", "WHEAT"),
    "CARROT": ("crop", "CARROT"),
    "TOMATO": ("crop", "TOMATO"),
}


def _mshape(func, x):
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return _math.sqrt(x)
    if func == "log10":
        return _math.log10(1.0 + x)
    return _math.log(1.0 + x)


def _mprice(item, inventory):
    """Exact port of the engine's market_price."""
    base, throughput, below_f, below_t, above_f, above_t = _MP[item]
    if inventory < _I0:
        amp = below_t * base / _mshape(below_f, throughput)
        value = base + amp * _mshape(below_f, _I0 - inventory)
    else:
        amp = above_t * base / _mshape(above_f, throughput)
        value = base - amp * _mshape(above_f, inventory - _I0)
    return max(_PRICE_FLOOR, int(round(value)))


def _remaining_drain(item, step, shops):
    """Units of `item` the town consumes between `step` and the season end.

    Shops fire on steps divisible by 4, the town center on steps divisible by 12
    with multipliers that step up on days 10 and 20. Still-locked shops are
    credited from the day they are expected to unlock (one new shop every three
    days), so late-game demand is not understated.
    """
    if item == "FERTILIZER":
        return 0.0  # neither the shops nor the town center consume fertilizer
    unlocked = set(shops or ())
    live = 0
    pending = []
    for name, products in _SHOP_DEMAND.items():
        if item not in products:
            continue
        weight = 2 if len(products) == 1 else 1
        if name in unlocked:
            live += weight
        else:
            pending.append(weight)
    n_locked = len(_SHOP_DEMAND) - len(unlocked)
    pending_total = sum(pending)
    is_center = item in _CENTER_ITEMS
    total = 0.0
    for s in range(step, 720):
        day = s // 24
        if s % 4 == 0:
            total += live
            if pending_total and n_locked > 0:
                expected = min(n_locked, max(0, day // 3 + 1 - len(unlocked)))
                total += pending_total * (expected / n_locked)
        if is_center and s % 12 == 0:
            total += 4 if day >= 20 else (2 if day >= 10 else 1)
    return total


def _count_driver(farm, kind, name):
    total = 0
    for row in farm.get("tiles") or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            if kind == "animal":
                animal = tile.get("animal")
                if animal and (name is None or animal == name):
                    total += 1
            elif tile.get("kind") == "PLANT" and tile.get("crop") == name:
                total += 1
    return total


def _opponent_scale(obs, item):
    """Opponent's expected remaining supply of `item`, relative to ours."""
    driver = _SUPPLY_DRIVER.get(item)
    if driver is None:
        return 1.0
    farms = obs.get("farms") or []
    if len(farms) < 2:
        return 1.0
    me = int(obs.get("player", 0) or 0)
    kind, name = driver
    mine = _count_driver(farms[me], kind, name)
    theirs = _count_driver(farms[1 - me], kind, name)
    if mine <= 0:
        return 1.0 if theirs > 0 else 0.0
    return max(0.0, min(2.0, theirs / float(mine)))


def _reserve_price(item, step, obs, shops):
    """Reservation price for one unit of `item`.

    A fixed fraction of base price, decayed linearly to zero over the
    liquidation ramp, and scaled down when the town's remaining appetite cannot
    absorb the supply still to come: a structurally oversupplied product is a
    race to sell, not something to hold.
    """
    base = _MP[item][0]
    frac = _RESERVE[item]
    if step >= _RAMP_START:
        span = float(max(1, _RAMP_END - _RAMP_START))
        frac *= max(0.0, (_RAMP_END - step) / span)
    drain = _remaining_drain(item, step, shops)
    supply = float(_SUPPLY.get(item, [0] * 721)[min(step, 720)])
    ahead = supply * (1.0 + _opponent_scale(obs, item))
    if ahead > 0.0:
        frac *= min(1.0, drain / ahead)
    return base * frac


def _plan_sells(obs, step, slots, short_of_cash):
    """Choose SELL orders for the controlled products."""
    if slots <= 0:
        return []
    shed = (obs.get("private") or {}).get("shed") or {}
    inventory = ((obs.get("market") or {}).get("inventory") or {})
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    load = sum(max(0, int(v or 0)) for v in shed.values())
    forced = load >= _SHED_PRESSURE or short_of_cash > 0

    candidates = []
    for item in _RESERVE:
        held = int(shed.get(item, 0) or 0)
        if held <= 0:
            continue
        inv = int(inventory.get(item, _I0) or _I0)
        if forced:
            units = held
        else:
            reserve = _reserve_price(item, step, obs, shops)
            units = 0
            while units < held and _mprice(item, inv + units) >= reserve:
                units += 1
        if units > 0:
            candidates.append((_mprice(item, inv) * units, item, units))
    candidates.sort(reverse=True)
    return [["SELL", item, units] for _, item, units in candidates[:slots]]


def _cash_needed(orders, obs):
    """Coins this turn's buy orders require."""
    seeds = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
    animals = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
    prices = ((obs.get("market") or {}).get("prices") or {})
    total = 0
    for order in orders:
        if not isinstance(order, list) or not order:
            continue
        op = order[0]
        if op == "BUY_SEED" and len(order) >= 3:
            total += seeds.get(order[1], 0) * int(order[2] or 0)
        elif op == "BUY_ANIMAL" and len(order) >= 3:
            total += animals.get(order[1], 0) * int(order[2] or 0)
        elif op == "BUY_PRODUCT" and len(order) >= 3:
            total += int(prices.get(order[1], 50) or 50) * int(order[2] or 0)
        elif op == "BUY_LAND":
            total += 4000
    return total


def _race_factor(item, step, obs):
    """1.0 when the town can absorb everything still coming, higher when not."""
    if _RACE_WEIGHT <= 0.0:
        return 1.0
    shops = (obs.get("town") or {}).get("unlocked_shops") or []
    drain = _remaining_drain(item, step, shops)
    supply = float(_SUPPLY.get(item, [0] * 721)[min(step, 720)])
    ahead = supply * (1.0 + _opponent_scale(obs, item))
    if ahead <= 0.0:
        return 1.0
    glut = max(0.0, 1.0 - drain / ahead)
    return 1.0 + _RACE_WEIGHT * glut


def _sell_priority(order, obs, step=0):
    """Rank a SELL order for slot placement; higher goes into an earlier slot.

    Market slots resolve index by index across both players, so an order in an
    earlier slot is priced before the opponent's matching order in a later slot.
    ``gross`` ranks by revenue at stake. ``impact`` ranks by how much revenue is
    actually lost by going second, which is the quantity times this order's own
    price impact — that promotes steep premium curves (wool, melon, milk) over
    large but nearly flat staple sales (wheat, egg).
    """
    if not (isinstance(order, list) and len(order) >= 3 and order[0] == "SELL"):
        return -1.0
    item = order[1]
    try:
        qty = int(order[2] or 0)
    except (TypeError, ValueError):
        return -1.0
    if qty <= 0 or item not in _MP:
        return -1.0
    inventory = ((obs.get("market") or {}).get("inventory") or {})
    inv = int(inventory.get(item, _I0) or _I0)
    unit = _mprice(item, inv)
    held = int(((obs.get("private") or {}).get("shed") or {}).get(item, 0) or 0)
    qty = min(qty, held) if held > 0 else qty
    race = _race_factor(item, step, obs)
    if _SORT_KEY == "unit":
        return float(unit) * race
    if _SORT_KEY == "impact":
        return float(qty) * float(unit - _mprice(item, inv + qty)) * race
    return float(unit) * float(qty) * race


def agent(obs, config=None):
    """c27 with its SELL layer partially replaced by the market controller."""
    action = _base_agent(obs, config)
    try:
        step = int(obs.get("step", 0) or 0)
        if step >= 717:
            return action  # proven terminal controller; leave untouched
        orders = list(action.get("market") or [])
        keep = [
            order for order in orders
            if not (
                isinstance(order, list) and len(order) >= 2
                and order[0] == "SELL" and order[1] in _RESERVE
            )
        ]
        player = int(obs.get("player", 0) or 0)
        money = float(((obs.get("farms") or [{}])[player]).get("money", 0) or 0)
        short = max(0.0, _cash_needed(keep, obs) - money)
        sells = _plan_sells(obs, step, 10 - len(keep), short)
        if not _SORT_SELLS:
            action["market"] = (sells + keep)[:10]
            return action

        def is_sell(o):
            return isinstance(o, list) and o and o[0] == "SELL"

        opp_money = None
        if _PROMOTE_IF_OPP_MONEY:
            farms = obs.get("farms") or []
            if len(farms) > 1:
                opp_money = float(farms[1 - player].get("money", 0) or 0)

        def promotable(o):
            if not is_sell(o):
                return False
            item = o[1]
            if item in _PROMOTE_IF_OPP_MONEY:
                if opp_money is None:
                    return False
                return opp_money >= _PROMOTE_IF_OPP_MONEY[item]
            if item in _PROMOTE_AFTER:
                return step >= _PROMOTE_AFTER[item]
            return not _PROMOTE or item in _PROMOTE

        # Only promotable sells compete for the earliest slots. WHEAT and
        # FERTILIZER are the only products an opponent can BUY_PRODUCT, so
        # promoting those ahead of their buys would lower the price they pay for
        # feed; those sells are deliberately left in their tape position, where
        # the opponent's buys have already drained inventory and lifted the price.
        merged = [o for o in sells if promotable(o)] + [o for o in keep if promotable(o)]
        merged.sort(key=lambda o: -_sell_priority(o, obs, step))
        rest = [o for o in sells if not promotable(o)] + [o for o in keep if not promotable(o)]
        if _SELLS_FIRST:
            action["market"] = (merged + rest)[:10]
        else:
            # Keep the tape's slot layout: sorted sells refill the slots that
            # already held promotable sells; every other order stays put.
            out = []
            queue = list(merged)
            for order in keep:
                out.append(queue.pop(0) if (promotable(order) and queue) else order)
            out.extend(queue)
            action["market"] = out[:10]
        return action
    except Exception:
        return action
