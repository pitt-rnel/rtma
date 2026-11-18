function num_differences = compare_message_defs( legacy, compiled)

% num_differences = compare_message_defs( legacy, compiled)
%
% Compares two RTMA structures of the same message definitions, as the
% MATLAB bindings use them: LEGACY translated from C headers by
% TranslateRTMAConfigFiles2Matlab, and COMPILED returned by the function
% that pyrtma's compiler writes (python -m pyrtma.compile --matlab). Each
% can be the structure, a MAT file name, or a definitions function, by
% handle, name or path.
%
% Prints each difference and returns how many there are. Names that only
% the legacy core headers define (MM_READY, SUBSCRIPTION_OPTION, and the
% QUICKLOGGER spelling of QUICK_LOGGER) are listed as expected and not
% counted. See README.md.

legacy = load_defs( legacy);
compiled = load_defs( compiled);
num_differences = 0;

expected_legacy_only = {'MT.MM_READY', 'MT.SUBSCRIPTION_OPTION', ...
    'MDF.SUBSCRIPTION_OPTION', 'MID.QUICKLOGGER'};

% Message types, module IDs and host IDs: same names and values.
for section = {'MT', 'MID', 'HID'}
    compare_ids( section{1});
end

% Message data formats, by type, which ReadMessage and SendMessage use.
compare_templates( 'MESSAGE_HEADER', legacy.MESSAGE_HEADER, compiled.MESSAGE_HEADER);
names = intersect( fieldnames( legacy.MT), fieldnames( compiled.MT));
for i = 1 : numel( names)
    name = names{i};
    mt = compiled.MT.(name);
    compare_templates( ['MDF_by_MT{' name '}'], ...
        get_cell( legacy.MDF_by_MT, mt + 1), get_cell( compiled.MDF_by_MT, mt + 1));
    if( ~isequal( get_cell( legacy.MTN_by_MT, mt + 1), get_cell( compiled.MTN_by_MT, mt + 1)))
        report( 'MTN_by_MT{%s} differs', name);
    end
end

% Mex opcodes: every legacy opcode, with the same value.
if( ~isfield( legacy, 'mex_opcode')), legacy.mex_opcode = struct(); end
for name = fieldnames( legacy.mex_opcode)'
    if( ~isfield( compiled.mex_opcode, name{1}))
        report( 'mex_opcode.%s is only in the legacy definitions', name{1});
    elseif( legacy.mex_opcode.(name{1}) ~= compiled.mex_opcode.(name{1}))
        report( 'mex_opcode.%s: legacy %d, compiled %d', name{1}, ...
            legacy.mex_opcode.(name{1}), compiled.mex_opcode.(name{1}));
    end
end

% Hashes: RTMA.hash.<NAME> in both, for the same messages.
compare_hashes();

% Constants in both, with the same value.
if( ~isfield( legacy, 'defines')), legacy.defines = struct(); end
for name = intersect( fieldnames( legacy.defines), fieldnames( compiled.defines))'
    a = legacy.defines.(name{1});
    b = compiled.defines.(name{1});
    if( isnumeric( a) && isnumeric( b))
        same = double( a) == double( b);
    else
        same = isequal( a, b);
    end
    if( ~same), report( 'defines.%s differs', name{1}); end
end

fprintf( '%d difference(s)\n', num_differences);


    function compare_ids( section)
        a = legacy.(section);
        b = compiled.(section);
        if( isempty( a)), a = struct(); end
        if( isempty( b)), b = struct(); end
        for n = setdiff( fieldnames( a), fieldnames( b))'
            key = [section '.' n{1}];
            if( any( strcmp( key, expected_legacy_only)))
                fprintf( 'expected: %s is only in the legacy definitions\n', key);
            else
                report( '%s is only in the legacy definitions', key);
            end
        end
        for n = setdiff( fieldnames( b), fieldnames( a))'
            report( '%s.%s is only in the compiled definitions', section, n{1});
        end
        for n = intersect( fieldnames( a), fieldnames( b))'
            if( double( a.(n{1})) ~= double( b.(n{1})))
                report( '%s.%s: legacy %d, compiled %d', section, n{1}, a.(n{1}), b.(n{1}));
            end
        end
    end

    function compare_hashes()
        a = struct(); b = struct();
        if( isfield( legacy, 'hash') && isstruct( legacy.hash)), a = legacy.hash; end
        if( isfield( compiled, 'hash') && isstruct( compiled.hash)), b = compiled.hash; end
        for n = setdiff( fieldnames( b), fieldnames( a))'
            report( 'hash.%s is missing from the legacy definitions', n{1});
        end
        for n = setdiff( fieldnames( a), fieldnames( b))'
            if( any( strcmp( ['MT.' n{1}], expected_legacy_only)))
                fprintf( 'expected: hash.%s is only in the legacy definitions\n', n{1});
            else
                report( 'hash.%s is only in the legacy definitions', n{1});
            end
        end
        for n = intersect( fieldnames( a), fieldnames( b))'
            if( ~strcmpi( char( a.(n{1})), char( b.(n{1}))))
                report( 'hash.%s: legacy %s, compiled %s', n{1}, char( a.(n{1})), char( b.(n{1})));
            end
        end
    end

    function compare_templates( where, a, b)
        % The same class, size and fields, recursively, which gives the
        % same bytes when MatlabRTMA converts it.
        if( ~strcmp( class( a), class( b)))
            report( '%s: class %s in legacy, %s in compiled', where, class( a), class( b));
        elseif( ~isequal( size( a), size( b)))
            report( '%s: size %s in legacy, %s in compiled', where, mat2str( size( a)), mat2str( size( b)));
        elseif( isstruct( a))
            fa = fieldnames( a);
            fb = fieldnames( b);
            if( ~isequal( fa, fb))
                report( '%s: fields {%s} in legacy, {%s} in compiled', where, ...
                    strjoin( fa', ', '), strjoin( fb', ', '));
            else
                for k = 1 : numel( a)
                    for f = 1 : numel( fa)
                        compare_templates( sprintf( '%s(%d).%s', where, k, fa{f}), ...
                            a(k).(fa{f}), b(k).(fa{f}));
                    end
                end
            end
        end
    end

    function report( varargin)
        num_differences = num_differences + 1;
        fprintf( [varargin{1} '\n'], varargin{2:end});
    end
end


function value = get_cell( c, index)
if( index <= numel( c)), value = c{index}; else, value = []; end
end


function defs = load_defs( source)
if( isstruct( source))
    defs = source;
elseif( isa( source, 'function_handle'))
    defs = source();
else
    source = char( source);
    [folder, name, ext] = fileparts( source);
    if( strcmpi( ext, '.mat'))
        loaded = load( source, '-mat');
        defs = loaded.RTMA;
    elseif( strcmpi( ext, '.m'))
        previous = cd( folder);
        restore = onCleanup( @() cd( previous)); %#ok<NASGU>
        defs = feval( name);
    else
        defs = feval( source);
    end
end
end
