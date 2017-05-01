cd ..\HC_csv
 dirs = dir(fullfile('.','*.xlsx'));
    for  direc =dirs'
    delimiterIn = ',';
    baseFileName=direc.name
    files0 = dir(fullfile(baseFileName,'*csv.0*'));
    descriptor=[];
    for file = files0'
        filename = file.name;
        stimulusTonefile=fullfile(baseFileName,filename)
        stimP50= erp(stimulusTonefile,24,72,'max')-stimP50;
        stimN100=erp(stimulusTonefile,70,130,'min')-stimP50;
        stimP200=erp(stimulusTonefile,180,235,'max')-stimP50;
%        latN200=lat(stimulusTonefile,
        descriptor=[stimP50,stimN100,stimP200];
    end
        files1 = dir(fullfile(baseFileName,'*csv.1*'));
    for file = files1'
        filename = file.name;
        targetTonefile=fullfile(baseFileName,filename)
        targP50= erp(targetTonefile,24,72,'max')-targP50;
        targN100=erp(targetTonefile,70,130,'min')-targP50;
        targP200=erp(targetTonefile,180,235,'max')-targP50;
        targN200=erp(targetTonefile,205,315,'min')-targP50;
        targP3b= erp(targetTonefile,325,580,'max')-targP50;
        targSlow=erp(targetTonefile,460,680,'min')-targP50;
        %TestAnalysis = importdata(targetToneFile);
        descriptor=[descriptor, targP50,targN100,targP200,targN200,targP3b,targSlow];
    end
        files2 = dir(fullfile(baseFileName,'*csv.2*'));
    for file = files2'
        filename = file.name;
        distractorTonefile=fullfile(baseFileName,filename)
        distP50= erp(distractorTonefile,24,72,'max')-distP50;
        distN100=erp(distractorTonefile,70,130,'min')-distP50;
        distP3a= erp(distractorTonefile,325,500,'max')-distP50;
        descriptor=[descriptor, distP50,distN100,distP3a];
        
    end
    descriptor=[descriptor,0];
    dlmwrite('..\test.csv',descriptor,'delimiter',',','-append');
    end
cd ..\MatLabPrograms