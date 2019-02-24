
%% iMatlab Personal Library
% Record handler for the PEER-NGA database, *.AT2 files
% i.e.bal@pl.hanze.nl
% v3.0, October 2014

% OUTPUT
% record    : The acc. data
% dt        : delta-t in sec
% pga_step  : The data step at which the PGA occurs

% INPUT
% inputfile : The name of the inputfile
% listname  : Name to be used for creating a txt fle
% cutoff    : Cut the record between two thershold acceleration values
% peakresponse : Delete record some time after the PGA (if interested only with the peak response)
% jump : If the original record dt is too small, then you can jump and
%        increase the dt artificially

function [record dt pga_step]=iF_AT2_Record_Handler_without_SF(inputfile,listname,cutoff,peakresponse,jump)

% cutoff --> Cut very small accelerations to speed up (0= no cutoff, insert
% the cutoff acceleration value otherwise) the unit of cutoff is always g

    ScaleFactor=1;


delimiterIn = ' ';
headerlinesIn = 4;
A = importdata(inputfile,delimiterIn,headerlinesIn);
[a b c d e] = strread(A.textdata{4, 1}, '%d %d %s %s %s', 'delimiter', ' ');
dt=str2num(c{1,1});
stp=floor(0.02/dt);
tot=5*ceil(a/5);
accs=A.data;
REC_raw=9.81*ScaleFactor.*reshape(accs',tot,1);
pga=max(abs(REC_raw));

if jump==0
    record2=REC_raw;
elseif jump==1
    record2=REC_raw(1:stp:tot);
    dt=stp*dt;
end


if cutoff>0&&pga>cutoff*9.81
    bottom=min(find(record2>=cutoff*9.81));
    top=max(find(record2>=cutoff*9.81));
    record=record2(bottom:top);
else
    record=record2;
end

rsize=size(record,1);

% Find on which step the PGA occurs
rmax=max(record);
rmin=min(record);

if rmax>abs(rmin)
    pga_step=find(record==rmax);
else
    pga_step=find(record==rmin);
end

if peakresponse>0&&pga_step*2<=rsize
    record(pga_step:2+1:rsize,:)=[];
end









