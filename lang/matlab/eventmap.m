function eventmap( varargin)

% eventmap( EVENT1, State1, EVENT2, State2, ...)
% 
% Set a global event map that will be used to map an event to the next state
    
    global RTMA_runtime;

    num_events = nargin / 2;
    if( num_events ~= nargin / 2), error( 'eventmap needs an even number of arguments'); end
    EventMap = reshape( varargin, [2 num_events]);
    Events = EventMap(1,:);
    States = EventMap(2,:);
    RTMA_runtime.EventMap = cell2struct( States, Events, 2);
    
%     % If a state timeout has been set, check to make sure the eventmap
%     % includes a mapping for the TIMED_OUT message
%     if( ~isempty( RTMA_runtime.StateTimeout_TimerID))
%         if( strmatch( 'TIMED_OUT', Events))
%         else
%             error( [GetCurrentState() ': eventmap(): a state timeout has been set without providing mapping for TIMED_OUT']);
%         end
%     end
%     
%     % If a mapping for TIMED_OUT has been provided, make sure that a
%     % timeout has been set
%     if( strmatch( 'TIMED_OUT', Events))
%         if( isempty( RTMA_runtime.StateTimeout_TimerID))
%             error( [GetCurrentState() ': eventmap(): a mapping for TIMED_OUT has been provided without setting a state timeout']);
%         end
%     end
