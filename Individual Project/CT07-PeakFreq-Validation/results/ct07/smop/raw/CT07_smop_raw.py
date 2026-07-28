# Generated with SMOP  0.41
from libsmop import *
# 

    data=xlsread('Commercial Tensile Tests.xlsx','CT07')
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:1
    # Selection of Excel workbook containing worked values for the commercial
# AE system, as well as the sheet relative to the test sample
    
    # Selection of specific data from the sheet to be used for plotting
    t1=data(arange(),1)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:6
    stress=data(arange(),4)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:7
    strain=data(arange(),3)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:8
    time=data(arange(),5)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:9
    rms=data(arange(),9)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:10
    cumrms=data(arange(),10)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:11
    energy=data(arange(),12)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:12
    cumenergy=data(arange(),14)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:13
    fig1=copy(figure)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:15
    
    plot(strain,stress,'b')
    ylabel('Stress (MPa)')
    xlabel('Strain (%)')
    ylim(concat([0,520]))
    title('T07 Strain vs. Stress')
    grid('minor')
    fig2=copy(figure)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:23
    yyaxis('left')
    plot(t1,stress,'b')
    ylabel('Stress (MPa)')
    xlabel('Time (s)')
    ylim(concat([0,max(stress)]))
    xlim(concat([0,250]))
    yyaxis('right')
    plot(time,rms,'r')
    ylim(concat([0,1.05]))
    ylabel('Normalised RMS (a.u.)')
    title('T09 Commercial Normalised RMS Profile')
    grid('minor')
    fig3=copy(figure)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:38
    yyaxis('left')
    plot(t1,stress,'b')
    ylabel('Stress (MPa)')
    xlabel('Time (s)')
    ylim(concat([0,max(stress)]))
    xlim(concat([0,300]))
    yyaxis('right')
    plot(time,cumrms,'r')
    ylim(concat([0,1.05]))
    ylabel('Normalised Cumulative RMS (a.u.)')
    title('T07 Commercial Normalised Cumulative RMS')
    grid('minor')
    fig4=copy(figure)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:53
    yyaxis('left')
    plot(t1,stress,'b')
    ylabel('Stress (MPa)')
    xlabel('Time (s)')
    ylim(concat([0,max(stress)]))
    xlim(concat([0,300]))
    yyaxis('right')
    scatter(time,energy,5,'filled','r')
    ylabel('Normalised AE Energy (a.u.)')
    ylim(concat([0,1.05]))
    title('T07 Commercial Normalised AE Energy')
    grid('minor')
    fig5=copy(figure)
# /Users/vangogh/Documents/毕设/初始数据&Matlab脚本/CT07.m:68
    yyaxis('left')
    plot(t1,stress,'b')
    ylabel('Stress (MPa)')
    xlabel('Time (s)')
    ylim(concat([0,max(stress)]))
    xlim(concat([0,300]))
    yyaxis('right')
    plot(time,cumenergy,'r')
    ylabel('Normalised Cumulative AE Energy (a.u.)')
    ylim(concat([0,1.05]))
    title('T07 Commercial Normalised Cumulative AE Energy')
    grid('minor')