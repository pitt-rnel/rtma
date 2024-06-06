% build core_defs to .mat (minimum message defs to test ConnectToMMM)
function build_core_defs()
RTMAPath = fullfile('..', '..');
TranslateRTMAConfigFiles2Matlab(RTMAPath, '', 'RTMACoreDefs');
end