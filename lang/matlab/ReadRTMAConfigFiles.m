% ReadRTMAConfigFiles( RTMA_BaseDir, File1, File2, ...)
%
% Reads core message definition files from the RTMA base directory (RTMA_BaseDir)
% plus optionally any additional user specified files to get the host and module id-s, and
% message type id-s, and message header and data structures. If RTMA_BaseDir is empty,
% then only reads the specified files.
%
% Meel Velliste
% 4/19/2006
% Amended 9/8/2008 to add flexibility to remove dependency on RTMA being installed
% in a fixed relative location to application modules. MV

function RTMA = ReadRTMAConfigFiles( RTMA_BaseDir, varargin)
    
    % Process argument list
    InputFilenames = {};
    for i = 1 : length( varargin)
        arg = varargin{i};
        % Make sure arguments are strings
        if( ~ischar(arg)), error( 'ReadRTMAConfigFiles() only takes string arguments'); end
        InputFilenames(end+1) = {arg};
    end
    
    FilePaths = {};

    % If RTMA base directory provided, then add core definition file to the list
    if( ~isempty( RTMA_BaseDir))
        FilePaths(end+1) = {fullfile(RTMA_BaseDir,'include','RTMA_types.h')};
    end

    % Add user defined files to the list
    FilePaths = [InputFilenames FilePaths];
    
    % Parse the file list
    h = ParseHFile( FilePaths{:});

    RTMA.HID = []; % Host ID-s
    RTMA.MID = []; % Module ID-s
    RTMA.MT = [];  % Message Types
    RTMA.MDF = [];  % Message Data Formats

    % Go through the defines and find the host ID-s (HID), module ID-s (MID)
    % and message types (MT), then find the messgae data formats (MDF) in
    % the tyepdefs
    RTMA = ExtractFields( h.defines, RTMA);
    RTMA = ExtractFields( h.typedefs, RTMA);

    % Check that all HID, MID and MT values are numeric
    CheckNumericIDs( RTMA);
    
    % Check for duplicate message types
    CheckDupes( RTMA.MT);

    % Message header template for the ReadMessage and SendMessage functions
    RTMA.MESSAGE_HEADER = h.typedefs.RTMA_MSG_HEADER;

    % Create a lookup table to get Message Type Name by Message Type ID
    RTMA.MTN_by_MT = {};
    message_names = fieldnames( RTMA.MT);
    for i = 1 : length( message_names)
        message_name = message_names{i};
        message_type_id = RTMA.MT.(message_name);
        RTMA.MTN_by_MT{message_type_id+1,1} = message_name;
    end

    % Create a lookup table to get Message Data Format by Message Type ID
    RTMA.MDF_by_MT = cell( size( RTMA.MTN_by_MT));
    message_names = fieldnames( RTMA.MDF);
    for i = 1 : length( message_names)
        message_name = message_names{i};
        % Make sure there is a matching MT field
        if( ~isfield( RTMA.MT, message_name))
            error( ['MDF_' message_name ' does not have a matching MT_' message_name ' defined']);
        end
        message_type_id = RTMA.MT.(message_name);
        RTMA.MDF_by_MT{message_type_id+1,1} = RTMA.MDF.(message_name);
    end

    % If RTMA base directory provided, then parse mex op-code definition file
    % to get the op-codes for calling the MatlabRTMA mex file
    if( ~isempty( RTMA_BaseDir))
        %MatlabRTMA_h = ParseHFile( [RTMA_BaseDir '/RTMA/lang/matlab/MatlabRTMA.h']);
        MatlabRTMA_h = ParseHFile( [RTMA_BaseDir '/lang/matlab/MatlabRTMA.h']);
        RTMA.mex_opcode = MatlabRTMA_h.defines;
    end
    
    % Put the raw parsed h-file content in the RTMA struct as well in case
    % we want to access some of the non-RTMA-specific defines
    RTMA.defines = h.defines;
    RTMA.typedefs = h.typedefs;
    RTMA.vars = h.vars;
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function RTMA = ExtractFields( fields, RTMA)

    names = fieldnames( fields);
    for n = 1 : length( names)
        name = names{n};
        [prefix, remainder] = strtok( name, '_');
        realname = remainder( 2:end);
        value = fields.(name);

        % Check that HID, MID and MT fields are integer values
        switch( prefix)
            case {'HID','MID','MT'}
                if( value ~= int32( value))
                    error('HID_, MID_ and MT_ values should be integers');
                end
        end

        % Put the fields and their values in the appropriate fields of the RTMA
        % structure
        if (any(strcmp(prefix,{'HID','MID','MT','MDF'})))
            RTMA.(prefix).(realname) = value; 
        end
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function CheckNumericIDs( Struct)

    id_types = {'HID', 'MID', 'MT'};

    for t = 1 : length( id_types)
        id_type = id_types{t};
        Names = fieldnames( Struct.(id_type));
        Values = struct2cell( Struct.(id_type));
        for i = 1 : length( Values)
            value = Values{i};
            switch( class( value))
                case 'double'
                otherwise
                    error( ['Value for ' id_type '_' Names{i} ' is not numeric: "' value '"']);
            end
        end
    end 
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function CheckDupes( Struct)

    %Names = fieldnames( Struct);
    ValuesCell = struct2cell( Struct);
    Values = [ValuesCell{:}];
    UniqueValues = unique( Values);
    NumValues = length( Values);
    NumUnique = length( UniqueValues);
    if( NumValues ~= NumUnique)
        sortedValues = sort(Values);
        idx = diff(sortedValues) == 0; %find(diff(sortedValues) == 0);
        error([ 'Duplicate message type ID-s found: ' num2str(sortedValues(idx)) ]);
    end
    
