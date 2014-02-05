function ShowError( msg)

% ShowError( msg)
%
% Prints out the latest error using some nicer formatting than the regular
% matlab error function. MSG is an additional message printed before the
% error text.

fprintf('\n');
disp('======================E R R O R===================================');
% Display the message if any
if( exist( 'msg', 'var'))
    disp( msg);
end
% Display the error message and its identifier
LastError = lasterror();
disp( LastError.message);
disp( LastError.identifier);
% Display the call stack
disp( 'Call stack:');
for i = 1 : length( LastError.stack)
    disp( ['    ' LastError.stack(i).name ': ' num2str(LastError.stack(i).line)]);
end
disp('==================================================================');
