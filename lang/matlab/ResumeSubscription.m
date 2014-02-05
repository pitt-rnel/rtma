function ResumeSubscription( varargin)
    
    global RTMA;
    global RTMA_runtime;

    for i = 1 : nargin
    
        MessageType = varargin{i};
        
        % convert Message Type String to numeric Message Type ID
        MessageTypeNumber = MessageTypeID_from_String( MessageType);
        
        % tell MM to resume sending this message type
        status = MatlabRTMA( RTMA.mex_opcode.RESUME_SUBSCRIPTION, MessageTypeNumber);
        if( status == 0), error( 'ResumeSubscription mex-function failed'); end

        % Remove the record from the paused subscriptions list
        idx = strmatch( MessageType, RTMA_runtime.Paused, 'exact');
        RTMA_runtime.Paused(idx,:) = [];
        
    end
