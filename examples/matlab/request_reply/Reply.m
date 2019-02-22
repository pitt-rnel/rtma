function Reply(mm_ip)

    global RTMA;

    RTMA_BaseDir = '../../..';
    addpath([RTMA_BaseDir '/lang/matlab']);

    RTMA_BaseDir

    MessageTypes =  { ...
                        'REQUEST_TEST_DATA' ...
                        'EXIT' ...
                    };

    ConnectArgs = {'REPLY', RTMA_BaseDir, ['./message_defs.mat']};
    if exist('mm_ip','var') && ~isempty(mm_ip)
        ConnectArgs{end+1} = ['-server_name ' mm_ip];
    end

    ConnectToMMM(ConnectArgs{:});
    Subscribe( MessageTypes{:})
    
    disp 'Reply running..'

    cnt = 1;
    while( 1)
        fprintf('\nWaiting for message\n');
        M = ReadMessage( 'blocking');
        
        switch(M.msg_type)
            case 'REQUEST_TEST_DATA'
                fprintf('Received message %s\n', M.msg_type);
            
                msg = RTMA.MDF.TEST_DATA;
                msg.a = int32(cnt);
                msg.b = int32(-30);
                msg.x = 123.456;
                SendMessage( 'TEST_DATA', msg);
                
                fprintf('Sent reply\n');
                cnt = cnt + 1;
            case 'EXIT'
                break; 

        end

    end

    DisconnectFromMMM

