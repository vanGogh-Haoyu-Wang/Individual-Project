clear all; clc
tic

[file_list, path_n] = uigetfile('.mat', 'Choose files', MultiSelect='on');
if iscell(file_list) == 0 
    file_list = (file_list);
end

fprintf('%s\n',"Loading Data")

D = [];
for i = 1:length(file_list)
    filename = file_list{i};
    v{i} = load(filename, 'data');
    D = [D; v{i}]; 
end

fprintf('%s\n', "Formatting Data")

blank = zeros(1e6,1);
P = [];
R = [];
for k = 1:i
    d = D(k).data(:,1);
    if k == 1
        avg_D = mean(d);
    end
    adj_data = d - avg_D; 
    adj_data = vertcat(adj_data, blank);
    if k == 1
        upthres = max(adj_data);
        lowthres = min(adj_data);
    end  
    mask = adj_data < upthres & adj_data > lowthres;
    adj_data(mask) = 0;
    Len = 200;
    movRMS = dsp.MovingRMS(Len,+1); 
    y = movRMS(adj_data);
    P = [P; y]; 
    adj = (num2cell(buffer(adj_data,200,1),1));
    R = [R, adj(1:end-1)];
end 

fprintf('%s\n',"Permforming DFT")

time = i*6;
x = linspace(0,time, length(P));


[peaks, maxVal] = find(P > 0.1);
val = R(peaks);
times = peaks(:)*(200/1e6);

E = []; 
for ii = 1:length(val)
    event = val(ii);
    event = cell2mat(event);
    e = abs(fft(event));
    E = [E,e(1:100,:)];
end

f = 1e6/200*(0:200-1);
f = f(1:100)/1000;

fprintf('%s\n',"Finding Peaks")

F1 = [];
I1 = [];
for iii = 1:length(E)
    threshold = max(E(iii));
    [lx, fx] = findpeaks(E(:,iii),f, NPeaks=1,SortStr="descend", MinPeakDistance=20);
    F1 = [F1; fx];
    I1 = [I1; lx];
end

id1_1 = F1>0 & F1>200;
idx1_1 = F1>0&F1<200;
b1_1 = F1;
b1_1(id1_1) = nan;

id2_1 = F1>250 | F1<200 ;
idx2_1 = F1>200&F1<250;
b2_1 = F1;
b2_1(id2_1) = nan;

id3_1 = F1>325 | F1<250;
idx3_1 = F1>200&F1<300;
b3_1 = F1;
b3_1(id3_1) = nan;

id4_1 = F1>400 | F1<325;
idx4_1 = F1>325&F1<400;
b4_1 = F1;
b4_1(id4_1) = nan;

id5_1 = F1>501 | F1<400;
idx5_1 = F1<501&F1>400;
b5_1 = F1;


fprintf('%s\n','Plotting')


figure;
scatter(times,F1,5,'r','filled')
xlim([0 max(times)+10])
ylim([0 500])
xlabel("Time (s)")
ylabel("Peak Frequency (kHz)")
grid("minor")
title("Time vs. Peak Frequency - Tensile Example")

figure;
scatter(I1,F1,5,'r','filled')
xlim([0 max(I1)+50])
ylim([0 500])
xlabel("Magnitude")
ylabel("Peak Frequency (kHz)")
grid("minor")
title("Magnitude vs. Peak Frequency - Tensile Example")


figure;
scatter(times,b5_1,5,[0 0.4470 0.7410], "filled")
hold on
scatter(times,b4_1,5,[0.3010 0.7450 0.9330],'filled')
scatter(times,b3_1,5,[0.4660 0.6740 0.1880],'filled')
scatter(times,b2_1,5,[0.9290 0.6940 0.1250],'filled')
scatter(times,b1_1,5,[0.6350 0.0780 0.1840],'filled')
xlim([0 max(times)+10])
ylim([0 500])
xlabel("Time (s)")
ylabel("Peak Frequency (kHz)")
grid("minor")
legend(["FP","FB","Debond","Delam","MC"])
title("Peak Frequency Assessment - Compressive (Flexural) Example")

hold off

toc