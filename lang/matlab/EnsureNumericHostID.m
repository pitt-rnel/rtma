function HostID = EnsureNumericHostID( HostID)

    % If HostID is a string, converts it to a numeric host ID
    % based on the lookup table in the RTMA structure

    global RTMA;

    if( ischar( HostID))
        if( isfield( RTMA.HID, HostID))
            HostID = RTMA.HID.(HostID);
        else
            error( ['Unrecognized HostID: ' HostID]);
        end
    end
