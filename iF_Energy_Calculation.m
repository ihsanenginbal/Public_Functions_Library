%% iMatlab Personal Library
% Calculation of the Cummulative Hysteretic Energy inside 
% a Force-Deformation Hysteresis Loop 
% Author: Prof. Ihsan Engin BAL
% Hanze University of Applied Sciences, Groningen, Netherlands
% www.eqresearch.nl
% i.e.bal@pl.hanze.nl
% v4.0, September 2018

% OUTPUT
% CRes  : Cummulative result, which is the area inside the loop (unit is the same with the input data)

% INPUT
% TDBS   : 2 columns, n rows matrix, where the first column is Displacement
% and the second column is force


function CRes=iF_Energy_Calculation(TDBS)


%% USER INPUT DATA
% Data file, first column is forces in kN, second is displacements in m
data(:,2)=TDBS(:,1);     
data(:,1)=TDBS(:,2); 

%% START

    data_length=size(data,1);
    
    %% Find cross-zero points
    clear cross_points
    cross_count=1;
    cross_points(1)=1;
    
    for i=1:data_length-1
        
        if data(i+1,2)*data(i,2)<0
            cross_count=cross_count+1;
            cross_points(cross_count)=i+1;
        end
        
    end
    
    % Close the cycles by adding the last data point
    cross_points(size(cross_points,2)+1)=data_length;
    
    %% Cut each cycle and calculate the cummulative energy
    num_of_cycles=size(cross_points,2);
    data_index=0;
    
    for j=1:num_of_cycles-1
        %for j=2:2
        
        % Find the block length for the seperated cycle
        k_find(j)=cross_points(j+1)-cross_points(j);
        
        clear cum_left
        clear cum_right
        clear pospeak
        clear negpeak
        
        CRes(j)=0;
        
        % Find the peak of each cycle in positive and negative directions
        pospeak(j)=max(data(cross_points(j):cross_points(j+1),2));
        negpeak(j)=min(data(cross_points(j):cross_points(j+1),2));
        peak=max(pospeak,abs(negpeak));
        
        for m=1:k_find(j)
            CRes_left(m)=data(cross_points(j)+m-1,1)*data(cross_points(j)+m,2);
            CRes_right(m)=data(cross_points(j)+m-1,2)*data(cross_points(j)+m,1);
            
            % Keep an account on which data line you are on
            data_index=data_index+1;
            
            
            % Cummulative energy
            if data_index==1
                CRes(data_index)=(CRes_left(m)-CRes_right(m))*0.5;
            else
                CRes(data_index)=CRes(data_index-1)+(CRes_left(m)-CRes_right(m))*0.5;
            end
            
            % Find the indices of the positive peaks
            if negpeak(j)==data(data_index,2)
                negpeak_index(j)=data_index;
            end
            if pospeak(j)==data(data_index,2)
                pospeak_index(j)=data_index;
            end
            
        end
        
        
    end
    
%     %% List the indices of the positive peaks (take care if the #of peaks in two dirs is not the same)
%     pnum=size(pospeak_index,2);
%     nnum=size(negpeak_index,2);
%     num=max(pnum,nnum);
%     
%     if nnum<pnum
%         for ek=nnum+1:pnum
%             negpeak_index(1,ek)=0;
%         end
%     else
%         for ek=pnum+1:nnum
%             pospeak_index(1,ek)=0;
%         end
%     end
%     peak_index=max(pospeak_index,negpeak_index);
    
    
    % Add a last line to 'CRes' to make them the same size
    CRes(size(CRes,2)+1)=CRes(size(CRes,2));


        
        
        
        
        
        



