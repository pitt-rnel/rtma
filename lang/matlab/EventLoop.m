% EventLoop
%
% Waits for an event, gets the next state from a global event map
% and goes to the next state

    global RTMA_runtime;
    EventLoop_PrevState = '';
    
    while( 1)
        switch( class( RTMA_runtime.EventMap))
            case 'cell'
                if( ~isempty( RTMA_runtime.StateTimeout_TimerID))
                    error( [RTMA_runtime.EventLoop_CurrentState ': EventLoop: A state timeout timer has been set in a state that did not use "eventmap". SetStateTimeOut() is only meant for states that use "eventmap".']);
                end
                switch( RTMA_runtime.EventMap{1})
                    case 'ReturnFromSuperState'
                        EventLoop_NextState = RTMA_runtime.EventMap{2};
                        RTMA_runtime.EventMap = {EventLoop_NextState, []};
                        EventLoop_Event = [];
                        break
                    otherwise
                        EventLoop_NextState = RTMA_runtime.EventMap{1};
                        EventLoop_Event = RTMA_runtime.EventMap{2};
                        if( ~isempty( EventLoop_Event))
                            EventLoop_Signal = EventLoop_Event.msg_type;
                        else
                            EventLoop_Signal = '';
                        end
                end
            case 'struct'
                EventLoop_ExpectedEvents = fieldnames( RTMA_runtime.EventMap);
                EventLoop_Event = WaitFor( EventLoop_ExpectedEvents{:});
                EventLoop_Signal = EventLoop_Event.msg_type;
                EventLoop_NextState = RTMA_runtime.EventMap.(EventLoop_Signal);
            otherwise
                if( isempty(RTMA_runtime.EventMap))
                    error( 'RTMA_runtime.EventMap is uninitialized');
                else
                    error( 'RTMA_runtime.EventMap should be either a string, struct or cell array');
                end
        end
        CancelStateTimeOut( ); % Make sure that the timeout timer is not left lingering
        %fprintf( 'EventLoop:    %s    --->  %s\n', EventLoop_Signal, EventLoop_NextState);
        EventLoop_Arguments.Event = EventLoop_Event;
        EventLoop_Arguments.PrevState = EventLoop_PrevState;
        UpdateStateLog( EventLoop_NextState, GetAbsTime());
        RTMA_runtime.EventLoop_CurrentState(end+1) = {EventLoop_NextState}; % Push current state to stack of current state
        feval( EventLoop_NextState, EventLoop_Arguments);
        RTMA_runtime.EventLoop_CurrentState(end) = []; % Pop state that just finished from stack of current state
        EventLoop_PrevState = EventLoop_NextState;
    end
