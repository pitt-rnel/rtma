function ForceRTMADump()


   RTMA_BaseDir = getenv('RTMA');
   App_BaseDir = getenv('ROBOTAPP');
   
   ConnectToMMM( 'GRASP_PLAN_PROCESSOR', RTMA_BaseDir, [App_BaseDir '/Common/include/RTMA_config.mat']);

    SendModuleReady( );
    
    SendSignal('DUMP_MESSAGE_LOG');