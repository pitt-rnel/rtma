function ModuleID = EnsureNumericModuleID( ModuleID)

    % If ModuleID is a string, converts it to a numeric module ID
    % based on the lookup table in the RTMA structure

    global RTMA;

    if( ischar( ModuleID))
        if( isfield( RTMA.MID, ModuleID))
            ModuleID = RTMA.MID.(ModuleID);
        else
            error( ['Unrecognized ModuleID: ' ModuleID]);
        end
    end
