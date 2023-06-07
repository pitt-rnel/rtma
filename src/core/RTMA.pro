PIPE_DIR=PipeLib
BASE_DIR=../..
SOURCES=RTMA.cpp MyCException.cpp MyCString.cpp $$PIPE_DIR/SocketPipe.cpp $$PIPE_DIR/UPipe.cpp $$PIPE_DIR/Timing.cpp
;HEADERS=$$BASE_DIR/include/RTMA.h $$BASE_DIR/include/MyCException.h $$BASE_DIR/include/MyCString.h $$BASE_DIR/include/Timing.h $$BASE_DIR/include/internal/UPipe.h
INCLUDEPATH += $$BASE_DIR/include $$BASE_DIR/include/internal


CONFIG += release thread warn_on dll
# uncomment below to add debug info
#CONFIG += force_debug_info
CONFIG -= qt
TARGET = RTMA

unix {
UI_DIR = .ui
MOC_DIR = .moc
OBJECTS_DIR = .obj
DEFINES += USE_LINUX
TEMPLATE = lib
DESTDIR=$$BASE_DIR/lib
}

win32 {
TEMPLATE = lib
CONFIG += console
DEFINES -= UNICODE
DESTDIR = $$BASE_DIR/lib
}
