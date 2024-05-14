function test_rtma_logger
% run as test_rtma_logger()

ConnectToMMM(0, '', 'RTMACoreDefs.mat');
log = RTMA_Logger.getLogger('test_log');
log.setCommandWindowLevel(log.ALL);
log.setRtmaLevel(log.DEBUG);
log.warning('call from main');
subfunction_test();
log.info('just some info');
log.critical('oh no!');
end

function subfunction_test()
log = RTMA_Logger.getLogger('test_log');
log.debug('call from subfun');
log.error('error from subfun')
end