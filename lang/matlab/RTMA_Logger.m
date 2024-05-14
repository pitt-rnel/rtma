classdef RTMA_Logger < handle
    % RTMA Client Logger for Matlab
    % Modified version of log4m from file exchange
    % Compatible with pyrtma.client_logging

    %LOG4M This is a simple logger based on the idea of the popular log4j.
    %
    % Description: Log4m is designed to be relatively fast and very easy to
    % use. It has been designed to work well in a matlab environment.
    % Please contact me (info below) with any questions or suggestions!
    %
    %
    % Author:
    %       Luke Winslow <lawinslow@gmail.com>
    % Heavily modified version of 'log4matlab' which can be found here:
    %       http://www.mathworks.com/matlabcentral/fileexchange/33532-log4matlab
    %

    properties (Constant)
        NOTSET = 0;
        DEBUG = 10;
        INFO = 20;
        WARNING = 30;
        ERROR = 40;
        CRITICAL = 50;

        ALL = 0;
        WARN = 30;
        EXCEPTION = 40;
        FATAL = 50;
        OFF = 1000;

        %ALL = 0;
        %TRACE = 1;
        %DEBUG = 2;
        %INFO = 3;
        %WARN = 4;
        %ERROR = 5;
        %FATAL = 6;
        %OFF = 7;
    end

    properties(SetAccess = protected)
        name;
        fullpath = 'RTMA_Logger.log';  %Default file
        commandWindowLevel = RTMA_Logger.ALL;
        rtmaLevel = RTMA_Logger.INFO;
        logFileLevel = RTMA_Logger.OFF; %RTMA_Logger.INFO;
        logMsg
        msg_map
    end

    properties
        rich_console = true;
    end

    methods (Static)
        function obj = getLogger( logName, logPath )
            %GETLOGGER Returns instance unique logger object.
            %   PARAMS:
            %       logName - Name of this logger
            %       logPath - Relative or absolute path to desired logfile (Optional).
            %   OUTPUT:
            %       obj - Reference to singular logger object.
            %
            % call as RTMA_Logger.getLogger(logName, logPath)

            if ~exist('logName', 'var') || isempty(logName)
                logName = GetCallerName;
            end

            if ~exist('logPath', 'var')
                logPath = '';
            end

            if(nargin > 2)
                error('getLogger only accepts two parameter inputs');
            end

            persistent localObjs;
            obj = [];
            if ~isempty(localObjs)
                for i = 1:length(localObjs)
                    if isvalid(localObjs(i)) && strcmp(localObjs(i).name, logName)
                        obj = localObjs(i);
                        break
                    end

                end
            end
            if isempty(obj)
                obj = RTMA_Logger(logName, logPath);
                localObjs = [localObjs obj];
            end
        end

        function testSpeed( logPath )
            %TESTSPEED Gives a brief idea of the time required to log.
            %
            %   Description: One major concern with logging is the
            %   performance hit an application takes when heavy logging is
            %   introduced. This function does a quick speed test to give
            %   the user an idea of how various types of logging will
            %   perform on their system.
            %

            if nargin < 1
                logPath = 'RTMA_LoggerTest.log';
            end

            L = RTMA_Logger.getLogger('RTMA_LoggerTest', logPath);


            disp('1e4 logs when logging only to command window');

            L.setCommandWindowLevel(L.DEBUG)%(L.TRACE);
            L.setLogFileLevel(L.OFF);
            tic;
            for i=1:1e4
                L.debug('test');
            end

            disp('1e4 logs when logging only to command window');
            toc;

            disp('1e6 logs when logging is off');

            L.setCommandWindowLevel(L.OFF);
            L.setLogFileLevel(L.OFF);
            tic;
            for i=1:1e6
                L.info('test');
            end
            toc;

            disp('1e4 logs when logging to file');

            L.setCommandWindowLevel(L.OFF);
            L.setLogFileLevel(L.DEBUG);
            tic;
            for i=1:1e4
                L.warning('test');
            end
            toc;

        end
    end

    % static protected methods
    methods (Static, Access = protected)
        function flag = is_rtma_connected()
            global RTMA_runtime %#ok<*GVMIS>

            if isempty(RTMA_runtime)
                flag = false;
            else
                flag = RTMA_runtime.Connected;
            end
        end

        function set_rtma_disconnected()
            global RTMA_runtime
            RTMA_runtime.Connected = false;
        end

        function [name, file, line] = getCallerName()

            stack = dbstack(3, '-completenames');
            if isempty(stack)
                name = 'COMMAND_LINE';
                file = '';
                line = 1;
            else
                name = stack(1).name;
                file = stack(1).file;
                line = stack(1).line;
            end
        end
    end


    %% Public Methods Section %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    methods
        function setFilename(self,logPath)
            %SETFILENAME Change the location of the text log file.
            %
            %   PARAMETERS:
            %       logPath - Name or full path of desired logfile
            %

            if isempty(logPath)
                self.setLogFileLevel(self.OFF);
            else
                [fid,message] = fopen(logPath, 'a');

                if(fid < 0)
                    error(['Problem with supplied logfile path: ' message]);
                end
                fclose(fid);
            end

            self.fullpath = logPath;
        end


        function setCommandWindowLevel(self,loggerIdentifier)
            self.commandWindowLevel = loggerIdentifier;
        end


        function setLogFileLevel(self,logFileLevel)
            self.logFileLevel = logFileLevel;
        end

        function setRtmaLevel(self, rtmaLevel)
            self.rtmaLevel = rtmaLevel;
        end


        %% The public Logging methods %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % function trace(self, message)
        %     %TRACE Log a message with the TRACE level
        %     %
        %     %   PARAMETERS:
        %     %       funcName - Name of the function or location from which
        %     %       message is coming.
        %     %       message - Text of message to log.
        %     %
        %     self.writeLog(self.TRACE,message);
        % end

        function debug(self, message)
            %DEBUG Log a message with the DEBUG level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.DEBUG,message);
        end


        function info(self, message)
            %INFO Log a message with the INFO level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.INFO,message);
        end


        function warning(self, message)
            %WARNING Log a message with the WARNING level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.WARNING,message);
        end

        function warn(self, message)
            %WARN Log a message with the WARN level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.WARN,message);
        end

        function error(self, message)
            %ERROR Log a message with the ERROR level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.ERROR,message);
        end

        function exception(self, message)
            %EXCEPTION Log a message with the EXCEPTION level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.EXCEPTION,message);
        end

        function critical(self, message)
            %CRITICAL Log a message with the CRITICAL level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.CRITICAL,message);
        end

        function fatal(self, message)
            %FATAL Log a message with the FATAL level
            %
            %   PARAMETERS:
            %       funcName - Name of the function or location from which
            %       message is coming.
            %       message - Text of message to log.
            %
            self.writeLog(self.FATAL,message);
        end

    end

    %% Private Methods %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %   Unless you're modifying this, these should be of little concern to you.
    methods (Access = private)

        function self = RTMA_Logger(name, path)
            self.name = name;
            self.setFilename(path);
            self.genLogMessageTemplate();
            self.genMtMap();
        end

        function genMtMap(self)
            global RTMA
            rtma = RTMA;
            if isempty(rtma)
                rtma = LoadRtmaConfig;
            end
            keys = [self.DEBUG, self.INFO, self.WARNING, self.ERROR, self.CRITICAL, self.ALL];
            values = [rtma.MT.RTMA_LOG_DEBUG, ...
                rtma.MT.RTMA_LOG_INFO, ...
                rtma.MT.RTMA_LOG_WARNING, ...
                rtma.MT.RTMA_LOG_ERROR, ...
                rtma.MT.RTMA_LOG_CRITICAL, ...
                rtma.MT.RTMA_LOG];
            self.msg_map = containers.Map(keys, values);
        end

        function mt = get_msg_type(self, level)
            if isKey(self.msg_map, level)
                mt = self.msg_map(level);
            else
                mt = self.msg_map(self.ALL);
            end
        end

        function genLogMessageTemplate(self)
            global RTMA
            rtma = RTMA;
            if isempty(rtma)
                rtma = LoadRtmaConfig;
            end
            self.logMsg = rtma.MDF.RTMA_LOG;
            lenName = length(self.name);
            self.logMsg.name(1:lenName) = int8(self.name);
        end

        %% WriteToFile
        function writeLog(self,level,message)
            
            if(self.logFileLevel > level && self.commandWindowLevel > level && self.rtmaLevel > level)
                return
            end

            % datestr is faster than datetime('now','Format','yyyy-MM-dd HH:mm:ss.SSS')
            dstr = datestr(now,'yyyy-mm-dd HH:MM:SS.FFF'); %#ok<TNOW1,DATST>
            [funcName, file, lineno] = self.getCallerName;

            % set up our level string
            switch level
                %case{self.TRACE}
                %    levelStr = 'TRACE';
                case{self.DEBUG}
                    levelStr = 'DEBUG';
                    levelColor = 'green';
                case{self.INFO}
                    levelStr = 'INFO';
                    levelColor = 'blue';
                    %case{self.WARN}
                    %    levelStr = 'WARN';
                case{self.WARNING}
                    levelStr = 'WARNING';
                    levelColor = 'magenta';
                case{self.ERROR}
                    levelStr = 'ERROR';
                    levelColor = 'red';
                case{self.CRITICAL}
                    levelStr = 'CRITICAL';
                    levelColor = 'red';
                    %case{self.FATAL}
                    %    levelStr = 'FATAL';
                otherwise
                    levelStr = 'UNKNOWN';
            end

            % If necessary write to command window
            if ( self.commandWindowLevel <= level )

                if self.rich_console
                    cprintf('blue', '[%s] ', dstr);
                    cprintf(levelColor, '%s ',levelStr);
                    cprintf('#777777', '<%s>:%d  |  ', funcName, lineno);
                    cprintf('black', '%s\n', message);
                else
                    if level >= self.ERROR
                        fout = 2; %stderr
                    else
                        fout = 1; %stdout
                    end
                    fprintf(fout, '[%s] %s <%s>:%d  |  %s\r\n' ...
                        , dstr ...
                        , levelStr ...
                        , funcName ...
                        , lineno ... % Have left this one with the '.' if it is passed
                        , message);
                end
            end

            if self.rtmaLevel <= level
                self.sendRtmaLog(level, funcName, file, lineno, message);
            end


            %If currently set log level is too high, just skip this log
            if(self.logFileLevel > level)
                return;
            end

            % Append new log to log file
            try
                fid = fopen(self.fullpath,'a');
                fprintf(fid, '[%s] %s <%s>:%d  |  %s\r\n' ...
                    , dstr ...
                    , levelStr ...
                    , funcName ...
                    , lineno ... % Have left this one with the '.' if it is passed
                    , message);
                fclose(fid);
            catch ME_1
                display(ME_1); %#ok<DISPLAYPROG>
            end
        end

        function sendRtmaLog(self,level, funcName, file, lineno, message)
            global RTMA
            if self.is_rtma_connected
                try
                    msg = self.logMsg;
                    msg.time = posixtime(datetime('now','TimeZone','UTC'));
                    msg.level = int32(level);
                    msg.lineno = int32(lineno);
                    lenFile = min(length(file), 512);
                    msg.pathname(1:lenFile) = int8(file(1:lenFile));
                    lenFunc = min(length(funcName), 256);
                    msg.funcname(1:lenFunc) = int8(funcName(1:lenFunc));
                    lenMsg = min(RTMA.defines.CC_MAX_LOG_LENGTH, length(message));
                    msg.message(1:lenMsg) = int8(message(1:lenMsg));
                    SendMessage(self.get_msg_type(level), msg);
                catch
                    self.set_rtma_disconnected();
                end
            end
        end

    end

end

