% Nissan LEAF
% 403.2 volts/360 nominal
% 24 kWh/90 kW
% 3.3 kW (2013 upgrade to 6.6 kW?)
% more at: http://www.roperld.com/science/NissanLeaf.htm

%Battery
BATRESPONSETIME=10;
VBN=360;
PBN=24000;
RC=PBN/VBN; %Rated capacity (Ah@C1)
VBNmax=419.0354;  %From simulink model
VBNmin=350; %From design
SOCo=80;



