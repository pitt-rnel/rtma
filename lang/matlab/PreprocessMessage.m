function M = PreprocessMessage( M, ExpectedMessageTypes)

% M = PreprocessMessage( M, ExpectedMessageTypes)
%
% Proprocess a message when it is received from the Module's pipe, so as to
% call an event hook, act on common exit signals and deal with timer
% messages

% Meel Velliste, April 2006
    
    global RTMA_runtime;

    % Call event hook
    if( isfield( RTMA_runtime, 'EventHook'))
        M = feval( RTMA_runtime.EventHook, M);
    end
    
    if( ~isempty( M))
        switch( M.msg_type)
            case 'TIMER_EXPIRED'
                % If the expired timer belongs to a state timeout, then
                % convert the message to TIMED_OUT
                if( M.data.timer_id == RTMA_runtime.StateTimeout_TimerID)
                    M.msg_type = 'TIMED_OUT';
                    RTMA_runtime.StateTimeout_TimerID = [];
                end
            case 'EXIT', error( 'RTMA:EXIT', 'EXIT message received');
            case 'KILL', error( 'RTMA:KILL', 'KILL message received');
            case 'END', error( 'RTMA:END', 'END message received');
        end
        isAnExpectedMessage = ~isempty( strmatch( M.msg_type, ExpectedMessageTypes, 'exact'));
        if( ~isAnExpectedMessage)
            %disp( ['UNEXPECTED MESSAGE RECEIVED: ' M.msg_type ' (Message disregarded)']);
            M = [];
        end
    end
