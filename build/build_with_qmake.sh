#!/bin/bash

SRC_DIR="../src"

# generate Makefiles with qmake
qmake -o Makefile RTMADirs.pro
qmake -o "${SRC_DIR}/core/Makefile" "${SRC_DIR}/core/RTMA.pro"
qmake -o "${SRC_DIR}/modules/Makefile" "${SRC_DIR}/modules/Modules.pro"
qmake -o "${SRC_DIR}/modules/MessageManager/Makefile" "${SRC_DIR}/modules/MessageManager/MessageManager.pro"
qmake -o "${SRC_DIR}/modules/QuickLogger/Makefile" "${SRC_DIR}/modules/QuickLogger/QuickLogger.pro"

# run make
make
