function matlab_client( server, defs_file, out_file)

% matlab_client( server, defs_file, out_file)
%
% The MATLAB module of test_matlab.py. Connects to the message manager at
% server with a dynamic ID and the name 'matlab-client', using the
% definitions function defs_file that pyrtma compiled from
% interop.defs, sends a MATLAB_TEST_REQUEST, and waits for the
% MATLAB_TEST_REPLY. It subscribes to every type, and the test's peer
% sends a message of a type the definitions don't define first, which
% ReadMessage should skip with a warning.
%
% Writes key=value lines to out_file. Any error is reported there too, and
% MATLAB exits with an error, which matlab -batch turns into a nonzero
% exit status.

out = fopen( out_file, 'w');
closer = onCleanup( @() fclose( out));
try
    ConnectToMMM( 0, 'matlab-client', defs_file, '-server_name', server);
    global RTMA_runtime; %#ok<TLEV>
    fprintf( out, 'module_id=%d\n', RTMA_runtime.ModuleID);

    % Subscribe to every type, as a module receives messages of types its
    % definitions don't define only then (or as a logger). Subscribe takes
    % names the definitions define, so this calls the mex directly with
    % ALL_MESSAGE_TYPES.
    global RTMA; %#ok<TLEV>
    ALL_MESSAGE_TYPES = 2147483647;
    if( MatlabRTMA( RTMA.mex_opcode.SUBSCRIBE, ALL_MESSAGE_TYPES) == 0)
        error( 'could not subscribe to ALL_MESSAGE_TYPES');
    end
    pause( 0.2); % let the manager process the SUBSCRIBE before the reply

    request = RTMA.MDF.MATLAB_TEST_REQUEST;
    request.value = int32( 7);
    request.values = int32( [1 2 3]);
    SendMessage( 'MATLAB_TEST_REQUEST', request);
    fprintf( out, 'sent\n');

    % Other messages come first, such as the manager's ACK for the
    % SUBSCRIBE, which the client doesn't wait for. Read until the reply.
    lastwarn( '');
    reply = [];
    start = tic;
    while( isempty( reply) && toc( start) < 30)
        msg = ReadMessage( 1);
        if( isempty( msg)), continue; end
        if( strcmp( msg.msg_type, 'MATLAB_TEST_REPLY'))
            reply = msg;
        else
            fprintf( out, 'skipped=%s\n', msg.msg_type);
        end
    end
    if( isempty( reply)), error( 'no MATLAB_TEST_REPLY'); end
    [~, warning_id] = lastwarn();
    fprintf( out, 'reply_type=%s\n', reply.msg_type);
    fprintf( out, 'reply_value=%d\n', reply.data.value);
    fprintf( out, 'reply_values=%s\n', mat2str( double( reply.data.values)));
    fprintf( out, 'warning_id=%s\n', warning_id);

    DisconnectFromMMM;
    fprintf( out, 'disconnected\n');
catch err
    fprintf( out, 'error=%s\n', strrep( getReport( err, 'basic'), newline, ' '));
    rethrow( err);
end
