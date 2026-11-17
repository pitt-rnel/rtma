function hash = GetHash_by_MT( MessageType)

% hash = GetHash_by_MT( MessageType)
%
% Returns the definition hash of a numeric message type, which SendMessage
% and SendSignal put in the message header as its version, or 0 if the
% loaded message definitions have none for it. Receivers using pyrtma can
% check it against their own definitions.
%
% The hashes are in RTMA.hash.<NAME>, as strings of hex digits, in both
% definitions compiled by pyrtma and those translated from C headers by
% TranslateRTMAConfigFiles2Matlab. A MAT file translated before the
% translator added them has none, and its messages are sent with version 0,
% which receivers don't check.

global RTMA;
hash = 0;
name = GetMTN_by_MT( MessageType);
if( isempty( name) || ~isfield( RTMA, 'hash') || ~isstruct( RTMA.hash) || ...
        ~isfield( RTMA.hash, name))
    return;
end
hash = hex2dec( char( RTMA.hash.(name)));
