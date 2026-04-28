#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run MINEA.
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from minea import Minea


if __name__ == "__main__":

    QApplication.setApplicationName("Minea")
    QApplication.setOrganizationName("Minea")

    app = QApplication(sys.argv)
    # style_sheet = Path(__file__).parent.joinpath("minea", "ui", "style.qss")
    # if style_sheet.exists():
    #     with open(style_sheet) as fileobj:
    #         style = fileobj.read()
    # app.setStyleSheet(style)

    # set desktop file, if it exists
    # this allows the correct icon to be shown on wayland
    p = Path.home().joinpath(".local", "share", "applications", "minea.desktop")
    if p.exists():
        app.setDesktopFileName(str(p))

    window = Minea()
    window.show()

    sys.exit(app.exec())
