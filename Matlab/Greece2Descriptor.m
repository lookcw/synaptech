Fs = 250;

% HC ---------------------
cd HC_GD
cd HC_stanAvg
dirs  = dir(fullfile('.','*.csv'));
descriptorS=[];
for file = dirs'
    filename = file.name;
    stimulusTonefile=fullfile(filename)
    %stimP50 =erpn(stimulusTonefile,24, 72, 'max');
    %stimN100=erpn(stimulusTonefile,70, 130,'min');
    %stimP200=erpn(stimulusTonefile,180,235,'max');
    %stimN200=erpn(stimulusTonefile,120,340,'min'); % 120,340 % 205,315
    %stimP3a =erpn(stimulusTonefile,325,500,'max');
    %stimP3b =erpn(stimulusTonefile,280,680,'max'); % 280,680 % 325,580
    %stimSlow=erpn(stimulusTonefile,460,680,'min');
    lstimP50 =lat(stimulusTonefile,24, 72, 'max');
    lstimN100=lat(stimulusTonefile,70, 130,'min');
    lstimP200=lat(stimulusTonefile,180,235,'max');
    lstimN200=lat(stimulusTonefile,120,340,'min'); % 120,340 % 205,315
    %lstimSlow=lat(stimulusTonefile,460,680,'min');
    %lstimP3b =lat(stimulusTonefile,280,680,'max'); % 280,680 % 325,580
    %brazilstat_vector=brazilstat(stimulusTonefile);
%     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));

% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end
    
    %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,brazilstatMat_vector];
    %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimP50,lstimN100,lstimP200,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
    descriptorS = [descriptorS;lstimP50,lstimN100,lstimP200,lstimN200]; %,lstimSlow,lstimP3b];
end
cd ..

cd HC_targAvg
dirs  = dir(fullfile('.','*.csv'));
descriptorT=[];
for file = dirs'
    filename = file.name;
    stimulusTonefile=fullfile(filename)
    %stimP50 =erpn(stimulusTonefile,24, 72, 'max');
    %stimN100=erpn(stimulusTonefile,70, 130,'min');
    %stimP200=erpn(stimulusTonefile,180,235,'max');
    %stimN200=erpn(stimulusTonefile,120,340,'min');
    %stimP3a =erpn(stimulusTonefile,325,500,'max');
    %stimP3b =erpn(stimulusTonefile,280,680,'max');
    %stimSlow=erpn(stimulusTonefile,460,680,'min');
    lstimP50 =lat(stimulusTonefile,24, 72, 'max');
    lstimN100=lat(stimulusTonefile,70, 130,'min');
    lstimP200=lat(stimulusTonefile,180,235,'max');
    lstimN200=lat(stimulusTonefile,120,340,'min');
    %lstimSlow=lat(stimulusTonefile,460,680,'min');
    %lstimP3b =lat(stimulusTonefile,280,680,'max');
    %brazilstat_vector=brazilstat(stimulusTonefile);
%     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));

% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end

    %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,brazilstatMat_vector];
    %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimP50,lstimN100,lstimP200,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
    descriptorT = [descriptorT;lstimP50,lstimN100,lstimP200,lstimN200]; %,lstimSlow,lstimP3b];
end
cd ..
cd ..

descriptorST = [descriptorS,descriptorT];
Ind0 = {};
for n = 1:size(descriptorST,1)
    Ind0{n} = '-';
end
Ind0 = string(Ind0);
descriptorH = [descriptorST,Ind0'];
%dlmwrite('GreeceHC.csv',descriptor,'delimiter',',','-append');




% MCI --------------------
cd MCI_GD
cd MCI_stanAvg
dirs  = dir(fullfile('.','*.csv'));
descriptorS=[];
for file = dirs'
    filename = file.name;
    stimulusTonefile=fullfile(filename)
    %stimP50 =erpn(stimulusTonefile,24, 72, 'max');
    %stimN100=erpn(stimulusTonefile,70, 130,'min');
    %stimP200=erpn(stimulusTonefile,180,235,'max');
    %stimN200=erpn(stimulusTonefile,205,315,'min');
    %stimP3a =erpn(stimulusTonefile,325,500,'max');
    %stimP3b =erpn(stimulusTonefile,325,580,'max');
    %stimSlow=erpn(stimulusTonefile,460,680,'min');
    lstimP50 =lat(stimulusTonefile,24, 72, 'max');
    lstimN100=lat(stimulusTonefile,70, 130,'min');
    lstimP200=lat(stimulusTonefile,180,235,'max');
    lstimN200=lat(stimulusTonefile,205,315,'min');
    %lstimSlow=lat(stimulusTonefile,460,680,'min');
    %lstimP3b =lat(stimulusTonefile,325,580,'max');
    %brazilstat_vector=brazilstat(stimulusTonefile);
%     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));

% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end

    %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,brazilstatMat_vector];
    %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimP50,lstimN100,lstimP200,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
    descriptorS = [descriptorS;lstimP50,lstimN100,lstimP200,lstimN200]; %,lstimSlow,lstimP3b];
end
cd ..

cd MCI_targAvg
dirs  = dir(fullfile('.','*.csv'));
descriptorT=[];
for file = dirs'
    filename = file.name;
    stimulusTonefile=fullfile(filename)
    %stimP50 =erpn(stimulusTonefile,24, 72, 'max');
    %stimN100=erpn(stimulusTonefile,70, 130,'min');
    %stimP200=erpn(stimulusTonefile,180,235,'max');
    %stimN200=erpn(stimulusTonefile,205,315,'min');
    %stimP3a =erpn(stimulusTonefile,325,500,'max');
    %stimP3b =erpn(stimulusTonefile,325,580,'max');
    %stimSlow=erpn(stimulusTonefile,460,680,'min');
    lstimP50 =lat(stimulusTonefile,24, 72, 'max');
    lstimN100=lat(stimulusTonefile,70, 130,'min');
    lstimP200=lat(stimulusTonefile,180,235,'max');
    lstimN200=lat(stimulusTonefile,205,315,'min');
    %lstimSlow=lat(stimulusTonefile,460,680,'min');
    %lstimP3b =lat(stimulusTonefile,325,580,'max');
    %brazilstat_vector=brazilstat(stimulusTonefile);
%     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));

% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end

    %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,brazilstatMat_vector];
    %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimP50,lstimN100,lstimP200,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
    descriptorT = [descriptorT;lstimP50,lstimN100,lstimP200,lstimN200]; %,lstimSlow,lstimP3b];
end
cd ..
cd ..

descriptorST = [descriptorS,descriptorT];
Ind2 = {};
for n = 1:size(descriptorST,1)
    Ind2{n} = '+';
end
Ind2 = string(Ind2);
descriptorM = [descriptorST,Ind2'];
%dlmwrite('GreeceHC.csv',descriptor,'delimiter',',','-append');




% % AD ---------------------
% cd AD_stan
% dirs  = dir(fullfile('.','*.csv'));
% descriptorS=[];
% for file = dirs'
%     filename = file.name;
%     stimulusTonefile=fullfile(filename)
%     stimP50= erpn(stimulusTonefile,24, 72, 'max');
%     stimN100=erpn(stimulusTonefile,70, 130,'min');
%     stimP200=erpn(stimulusTonefile,180,235,'max');
%     stimN200=erpn(stimulusTonefile,120,340,'min');
%     stimP3a= erpn(stimulusTonefile,325,500,'max');
%     stimP3b= erpn(stimulusTonefile,280,680,'max');
%     stimSlow=erpn(stimulusTonefile,460,680,'min');
%     lstimP50 =lat(stimulusTonefile,24, 72, 'max');
%     lstimN100=lat(stimulusTonefile,70, 130,'min');
%     lstimP200=lat(stimulusTonefile,180,235,'max');
%     lstimN200=lat(stimulusTonefile,120,340,'min');
%     lstimSlow=lat(stimulusTonefile,460,680,'min');
%     lstimP3b =lat(stimulusTonefile,280,680,'max');
%     brazilstat_vector=brazilstat(stimulusTonefile);
% %     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));
% 
% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end
% 
%     %descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,brazilstatMat_vector];
%     descriptorS = [descriptorS;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimP50,lstimN100,lstimP200,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
%     %descriptorS = [descriptorS;lstimN200,lstimSlow,lstimP3b];
% end
% cd ..
% 
% cd AD_targ
% dirs  = dir(fullfile('.','*.csv'));
% descriptorT=[];
% for file = dirs'
%     filename = file.name;
%     stimulusTonefile=fullfile(filename)
%     stimP50 =erpn(stimulusTonefile,24, 72, 'max');
%     stimN100=erpn(stimulusTonefile,70, 130,'min');
%     stimP200=erpn(stimulusTonefile,180,235,'max');
%     stimN200=erpn(stimulusTonefile,120,340,'min');
%     stimP3a =erpn(stimulusTonefile,325,500,'max');
%     stimP3b =erpn(stimulusTonefile,280,680,'max');
%     stimSlow=erpn(stimulusTonefile,460,680,'min');
%     lstimP50 =lat(stimulusTonefile,24, 72, 'max');
%     lstimN100=lat(stimulusTonefile,70, 130,'min');
%     lstimP200=lat(stimulusTonefile,180,235,'max');
%     lstimN200=lat(stimulusTonefile,120,340,'min');
%     lstimSlow=lat(stimulusTonefile,460,680,'min');
%     lstimP3b =lat(stimulusTonefile,280,680,'max');
%     brazilstat_vector=brazilstat(stimulusTonefile);
% %     brazilstatMat_vector=brazilStatMat(bands(stimulusTonefile));
% 
% E=[];
% tandDat = importdata(stimulusTonefile);
% [row,col] = size(tandDat);
% for k = 2:col
%     FF = tandDat(:,k);
%     N = length(FF);
%     xdft = fft(FF);
%     xdft = xdft(1:N/2+1);
%     psdx = (1/(Fs*N)) * abs(xdft).^2;
%     psdx(2:end-1) = 2*psdx(2:end-1);
%     fftval = psdx';
%     E = [E,fftval];
% end
% 
%     %descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,brazilstatMat_vector];
%     descriptorT = [descriptorT;stimP50,stimN100,stimP200,stimN200,stimP3a,stimP3b,stimSlow,lstimP50,lstimN100,lstimP200,lstimN200,lstimSlow,lstimP3b,brazilstat_vector,E];
%     %descriptorT = [descriptorT;lstimN200,lstimSlow,lstimP3b];
% end
% cd ..
% 
% descriptorST = [descriptorS,descriptorT];
% Ind1 = {};
% for n = 1:size(descriptorST,1)
%     Ind1{n} = '+';
% end
% Ind1 = string(Ind1);
% descriptorA = [descriptorST,Ind1'];
% %dlmwrite('GreeceAD.csv',descriptor,'delimiter',',','-append');




% Labels -----------------
labels = {};
for k = 1:size(descriptorST,2)
    labels{k} = strcat('col',num2str(k));
end
labels{size(descriptorST,2)+1} = 'Indicator';
labels = string(labels);


% Descriptor Matrix ------
descriptor = [descriptorH;descriptorM]; %;descriptorA];
labdesc = [labels;descriptor];
fid=fopen('GD_lat_HCvMCI.csv','wt');
[rows,cols]=size(labdesc);
for k = 1:rows
    fprintf(fid,'%s,',labdesc{k,1:end-1});
    fprintf(fid,'%s\n',labdesc{k,end});
end
fclose(fid);

