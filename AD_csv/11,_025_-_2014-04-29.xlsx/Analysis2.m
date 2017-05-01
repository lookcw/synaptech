if exist('NewTest','var')~=1
    NewTest = importdata('11,_025_-_2014-04-29.xlsx.csv.2');
end
%%
if exist('tcsv0','var')~=1
   tcsv0 = importdata('11,_025_-_2014-04-29.xlsx.csv.1');
   tcsv0 = tcsv0(:,1:8);
end
%%

rawdata = tcsv0';
E1 = rawdata(2,:);
E2 = rawdata(3,:);
E3 = rawdata(4,:);
E4 = rawdata(5,:);
E5 = rawdata(6,:);
E6 = rawdata(7,:);
E7 = rawdata(8,:);

S = length(E1);
avgVal1 = zeros(S,1);
for n=10:S
    avgVal1(n-5) = (E1(n)+E1(n-1)+E1(n-2)+E1(n-3)+E1(n-4)+E1(n-5)+E1(n-6)+E1(n-7)+E1(n-8)+E1(n-9))/10;
end
avgVal2 = zeros(S,1);
for n=10:S
    avgVal2(n-5) = (E2(n)+E2(n-1)+E2(n-2)+E2(n-3)+E2(n-4)+E2(n-5)+E2(n-6)+E2(n-7)+E2(n-8)+E2(n-9))/10;
end
avgVal3 = zeros(S,1);
for n=10:S
    avgVal3(n-5) = (E3(n)+E3(n-1)+E3(n-2)+E3(n-3)+E3(n-4)+E3(n-5)+E3(n-6)+E3(n-7)+E3(n-8)+E3(n-9))/10;
end

figure
t = rawdata(1,:);
plot(t,E1); hold on
plot(t,avgVal1); grid on
hold on

plot(t,E2); hold on
plot(t,avgVal2); grid on
hold on

plot(t,E3); hold on
plot(t,avgVal3); grid on

N100index= find(t>=70 & t<=130);
N100val = abs(min(E1(N100index)));

N200ind = find(t>=170 & t<=300);
N200min = min(E1(N200ind));
poststim = find(t>=0);
minInd = find(E1==min(E1(N200ind)))-poststim(1);
N200lat = minInd*(t(2)-t(1));
