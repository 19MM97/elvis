Fc = 2000; % switching frequency

Ton=0.1;
Tstart=0.5;
Tend=8;
%Vs = 350;
Vs_full=419.0354;

% boost converter
L = 50e-3;
R = 0.5;
Co = 1186.5e-6;%2200e-6;

% boost converter current controller
bw = 700;
Kpi = 2*pi*bw*L*5;
Kii = 5*R/L;

% boost converter voltage controller
bwv = 30;
Kpv = 2*pi*bwv*Co;
Kiv = 5;

Vo_ref = 565;
Imax = 250; % nissan leaf
VLmax = VBNmax;
VLmin = VBN-Vo_ref;