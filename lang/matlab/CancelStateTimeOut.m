function CancelStateTimeOut

    global RTMA_runtime;
        
    if(~isempty(RTMA_runtime.StateTimeout_TimerID))
        %disp( ['Canceling StateTimeOut: TimerID = ' num2str(RTMA_runtime.StateTimeout_TimerID)]);
        CancelTimer( RTMA_runtime.StateTimeout_TimerID );
        RTMA_runtime.StateTimeout_TimerID = [];
    end
    