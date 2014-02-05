function TranslateRTMAhFiles2dotNET( RTMA_BaseDir, config_file_basename, output_namespace)
% TranslateRTMAhFiles2dotNET( config_file_basename, output_namespace)
%
% Translates .h files C# and other .NET languages.
% i.e. RTMA_config.h and associated files.
% config_file_basename is just a base name, i.e. without a file extension,
% because file extension is automatically created for each output
% language.
% output_namespace is the .NET namespace name within which you want
% the output to be declared.

% Meel Velliste 9/02/2008
% Copyright (c) 2008 Meel Velliste, University of Pittsburgh. All rights
% reserved.

global IndentLevel;
global IndentNumSpaces;

IndentLevel = 0;
IndentNumSpaces = 4;

RTMA = ReadRTMAConfigFiles( RTMA_BaseDir, [config_file_basename '.h']);

Languages = {'C#','C++'};
FileExtensions = {'.cs','.NET.h'};
for i = 1 : length( Languages)
    L = Languages{i};
    E = FileExtensions{i};
    f = fopen( [config_file_basename E], 'wt');
    BeginNamespace( output_namespace, L, f);
    use_const = true;
    force_int = true;
    WriteClass( RTMA.MT, 'MT', L, f, use_const, force_int);
    WriteClass( RTMA.MID, 'MID', L, f, use_const, force_int);
    WriteClass( RTMA.HID, 'HID', L, f, use_const, force_int);
    WriteClass( RTMA.MDF, 'MDF', L, f);
    WriteClass( RTMA.MESSAGE_HEADER, 'MESSAGE_HEADER', L, f);
    WriteClass( RTMA.defines, 'defines', L, f, use_const);
    WriteClass( RTMA.typedefs, 'typedefs', L, f);
    %RTMA.MTN_by_MT
    %RTMA.MDF_by_MT
    EndNamespace( L, f);
    fclose( f);
end


function BeginNamespace( name, language, f)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% BeginNamespace( name, language, f) - write a begin namespace
%
global Indent;
switch( language)
    case 'C++',
        fprintf( f, [Indent 'namespace ' name ' {\n' ...
                     Indent '\n']);
    case 'C#'
        fprintf( f, [Indent 'namespace ' name '\n' ...
                     Indent '{\n']);
    case 'VB', error( 'Sorry, VB output not implemented yet');
    otherwise, error( 'Unrecognized language');
end
IncreaseIndent( );


function EndNamespace( language, f)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% EndNamespace( language, f) - write an end namespace
%
global Indent;
DecreaseIndent( );
switch( language)
    case 'C++', fprintf( f, [Indent '}\n\n']);
    case 'C#',  fprintf( f, [Indent '}\n\n']);
    case 'VB', error( 'Sorry, VB output not implemented yet');
    otherwise, error( 'Unrecognized language');
end


function WriteEnum( enum_definitions, enum_name, language, f)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WriteEnum( enum_definitions, enum_name, language, f) - Write an enumeration definition
%
% enum_definitions - a struct where field names are enum names and values are enum values
% enum_name - name of the enum in the output file
% language - a string that defines output language ("C++", "C#" or "VB")
% f - file handle of output file

global Indent;

% Begin the enum definition
switch( language)
    case 'C++'
        fprintf( f, [Indent 'public enum class' enum_name '\n' ...
                     Indent '{\n']);
    case 'C#'
        fprintf( f, [Indent 'public enum ' enum_name '\n' ...
                     Indent '{\n']);
    case 'VB', error( 'Sorry, VB output not implemented yet');
    otherwise, error( 'Unrecognized language');
end

% Write the defined values
IncreaseIndent( );
names = fieldnames( enum_definitions);
for i = 1 : length( names)
    name = names{i};
    value = enum_definitions.(name);
    if( value ~= int32(value)), error( 'Value not suitable for "enum"'), end
    if( i == length( names)), comma = ''; else comma = ','; end
    switch( language)
        case 'C++', fprintf( f, [Indent name ' = ' num2str(value) comma '\n']);
        case 'C#',  fprintf( f, [Indent name ' = ' num2str(value) comma '\n']);
    end
end
DecreaseIndent( );

% End the enum definition
switch( language)
    case 'C++', fprintf( f, [Indent '};\n\n']);
    case 'C#', fprintf( f, [Indent '}\n\n']);
end


function WriteClass( member_definitions, class_name, language, f, use_const, force_int)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WriteClass( member_definitions, class_name, language, f, const_int) - Write a class definition
%
% member_definitions - a struct whose field names are class member names and values serve as a template for the type definition of the member
% class_name - name of the class in the output file
% language - a string that defines output language ("C++", "C#" or "VB")
% f - file handle of output file
% use_const_int - optional argument. If present, and if "true", then all members will have type "const int" and the value will be written

global Indent;
global IndentLevel;

if( ~exist( 'use_const', 'var'))
    use_const = false;
end
if( ~exist( 'force_int', 'var'))
    force_int = false;
end

% Begin the class definition
switch( language)
    case 'C++'
        fprintf( f, [Indent 'ref class ' class_name '\n' ...
                     Indent '{\n' ...
                     Indent 'public:\n']);
    case 'C#'
        fprintf( f, [Indent 'public class ' class_name '\n' ...
                     Indent '{\n']);
    case 'VB', error( 'Sorry, VB output not implemented yet');
    otherwise, error( 'Unrecognized language');
end

% Write the defined values
IncreaseIndent( );
names = fieldnames( member_definitions);
for i = 1 : length( names)
    name = names{i};
    value = member_definitions.(name);
    if( use_const)
        if( force_int)
            if( value ~= int32(value)), error( 'Value not suitable for "const int"'), end
            type = 'int';
        else
            if( IsInteger( value))
                type = 'int';
            else
                type = 'double';
            end
        end
        if( ischar( value))
            value(value=='"') = []; % Eliminate quote characters because they will not work inside C++ or C# source code
            switch( language)
                case 'C++', fprintf( f, [Indent 'static const char ' name '[] = "' value '";\n']);
                case 'C#',  fprintf( f, [Indent 'public const string ' name ' = "' value '";\n']);
            end
        else
            switch( language)
                case 'C++', fprintf( f, [Indent 'static const ' type ' ' name ' = ' num2str(value) ';\n']);
                case 'C#',  fprintf( f, [Indent 'public const ' type ' ' name ' = ' num2str(value) ';\n']);
            end
        end
    else
        switch( language)
            case 'C++', WriteMemberCPP( name, value, f);
            case 'C#',  WriteMemberCS( name, value, f);
        end
    end
end
DecreaseIndent( );

% End the class definition
if( IndentLevel <= 2), extra_newline = '\n'; else extra_newline = ''; end
switch( language)
    case 'C++', fprintf( f, [Indent '};\n' extra_newline]);
    case 'C#',  fprintf( f, [Indent '}\n' extra_newline]);
end


function WriteMemberCS( name, value, f)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WriteMemberCS( name, value, f) - Write class member in C# notation
%
% name - Member name
% value - the type of the value is used to infer the .NET type

global Indent;
global IndentLevel;

matlab_type = class( value);

switch( matlab_type)
    case 'char'
        if( ~isempty(strfind( value, 'VARIABLE_LENGTH_ARRAY(')))
            matlab_type = value(23:end-1);
            value = [];
        else
            error( '"char" type not implemented');
        end
end

switch( matlab_type)
    case 'int8', type = 'sbyte';
    case 'int16', type = 'short';
    case 'int32', type = 'int';
    case 'int64', type = 'long';
    case 'uint8', type = 'byte';
    case 'uint16', type = 'ushort';
    case 'uint32', type = 'uint';
    case 'uint64', type = 'ulong';
    case 'double', type = 'double';
    case 'single', type = 'float';
    case 'struct'
        if( IndentLevel > 2)
            type = [name '_type'];
            WriteClass( value, type, 'C#', f);
            fprintf( f, [Indent 'public ' type ' ' name ' = new ' type '();\n\n']);
        else
            WriteClass( value, name, 'C#', f);
        end
        return
    otherwise, error( 'Unsupported type');
end

if( isempty( value)) % If value is empty, then it designates a variable length array
    fprintf( f, [Indent 'public ' type '[] ' name ';\n']);
else

    if( ~isvector( value)), error( 'Matrices are not yet supported, value must be scalar or vector'); end
    vector_length = length( value);
    if( vector_length > 1)
        initializing_zeros = repmat('0,',[1 vector_length]);
        initializing_zeros(end) = []; % Eliminate last comma
        fprintf( f, [Indent 'public ' type '[] ' name ' = {' initializing_zeros '};\n']);
    else
        fprintf( f, [Indent 'public ' type ' ' name ';\n']);
    end
end

  
function WriteMemberCPP( name, value, f)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% WriteMemberCPP( name, value, f) - Write class member in C++ notation
%
% name - Member name
% value - the type of the value is used to infer the .NET type

global Indent;

matlab_type = class( value);

switch( matlab_type)
    case 'char'
        if( ~isempty(strfind( value, 'VARIABLE_LENGTH_ARRAY(')))
            matlab_type = value(23:end-1);
            value = [];
        else
            error( '"char" type not implemented');
        end
end

switch( matlab_type)
    case 'int8', type = 'System::SByte';
    case 'int16', type = 'System::Int16';
    case 'int32', type = 'System::Int32';
    case 'int64', type = 'System::Int64';
    case 'uint8', type = 'System::Byte';
    case 'uint16', type = 'System::UInt16';
    case 'uint32', type = 'System::UInt32';
    case 'uint64', type = 'System::UInt64';
    case 'double', type = 'System::Double';
    case 'single', type = 'System::Single';
    case 'struct', WriteClass( value, name, 'C++', f); return
    otherwise, error( 'Unsupported type');
end

if( isempty( value)) % If value is empty, then it designates a variable length array
    fprintf( f, [Indent 'static array<' type '> ^' name ';\n']);
else

    if( ~isvector( value)), error( 'Matrices are not yet supported, value must be scalar or vector'); end
    vector_length = length( value);
    if( vector_length > 1)
        initializing_zeros = repmat('0,',[1 vector_length]);
        initializing_zeros(end) = []; % Eliminate last comma
        fprintf( f, [Indent 'static array<' type '> ^' name ' = {' initializing_zeros '};\n']);
    else
        fprintf( f, [Indent 'static ' type ' ' name ';\n']);
    end
end

        
function IncreaseIndent( )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

global IndentLevel;
global IndentNumSpaces;
global Indent;

IndentLevel = IndentLevel + 1;
if( IndentLevel > 10), error( 'IndentLevel > 10'); end
Indent = repmat( ' ', [1 IndentLevel*IndentNumSpaces]);


function DecreaseIndent( )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

global IndentLevel;
global IndentNumSpaces;
global Indent;

IndentLevel = IndentLevel - 1;
if( IndentLevel < 0), error( 'IndentLevel < 0'); end
Indent = repmat( ' ', [1 IndentLevel*IndentNumSpaces]);


function is_integer = IsInteger( value)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    if( value == int32(value))
        is_integer = true;
    else
        is_integer = false;
    end
    