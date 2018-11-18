%% iMatlab Personal Library
% Calculation of the Accleration Spectra  
% Author: Prof. Ihsan Engin BAL
% Hanze University of Applied Sciences, Groningen, Netherlands
% www.eqresearch.nl
% i.e.bal@pl.hanze.nl
% v12.0, October 2018

% OUTPUT
% T     : Period output of the spectra
% Sa    : Acceleration spectra in the input units

% INPUT
% dti   : Time intervals of the acceleration record
% acc   : Acceleration vector
% Tmax  : Max period for which the spectrum is created (sec)
% Tstep : Period steps (i.e. in every Tstep seconds)for which the spectrum is created (sec)
% kisi  : Damping (put 0.05 for 5% damping, for example) 


function [T Sa]=iF_Spectra(dti,acc,T_max,T_step,kisi)

    for i=1:1:T_max/T_step;
        T(i+1)=i*T_step;
        T(1)=0.0000001;
    end
    tot=size(acc,1);

    %build the time stpes for acc. time history
    for f=1:tot;
        delta(f)=f*dti;
    end


    for j=1:1:T_max/T_step+1;
        w(j)=2*pi/T(j);
        wd=w(j)*sqrt(1-kisi^2);

        %Parameters
        F=(sin(wd*dti))*exp(-kisi*w(j)*dti);
        E=(cos(wd*dti))*exp(-kisi*w(j)*dti);

        %Calculating Alfa and Beta values
        A11=E+(kisi*w(j)/wd)*F;
        A12=F/wd;
        A21=(-w(j).^2*A12);
        A22=E-(kisi*w(j)/wd)*F;
        B11=(A11-1)/(w(j).^2);
        B12=(A12-2*kisi*w(j)*B11-dti)/(w(j).^2*dti);
        B21=-A12;
        B22=B11/dti;

        u(1)=0;
        ud(1)=0;
        udd(1)=0;

        % Xi+1 = AXi + Bai
        for k=1:(length(acc)-1);
            u(k+1)=A11*u(k)+A12*ud(k)+B11*acc(k)+B12*(acc(k+1)-acc(k));
            ud(k+1)=A21*u(k)+A22*ud(k)+B21*acc(k)+B22*(acc(k+1)-acc(k));
            udd(k+1)=-(2*kisi*w(j)*ud(k+1)+(w(j)^2)*u(k+1));

        end

        % Find the max spectral values
        maks(j)=max(abs(u));
        maks1(j)=max(abs(ud));
        maks2(j)=max(abs(udd));

    end

    Sa=maks2';


end


















