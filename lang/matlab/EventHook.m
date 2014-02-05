function Message = EventHook( Message)

% Message = EventHook( Message)
%
% This function gets executed every time when a message is received through
% the WaitFor function. The default function does not do anything. An
% application can override this function to intercept messages before they
% are passed to the application.
%
% Meel Velliste
% 4/23/2006
