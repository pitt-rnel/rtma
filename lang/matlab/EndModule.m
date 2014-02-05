function EndModule

% EndModule
%
% Disconnects from RTMA and exits matlab
try
    fprintf( 'Module is exiting... ')
    DisconnectFromMMM
    disp( 'done!');
catch
    error( 'Failed disconnecting from RTMA');
end

exit
