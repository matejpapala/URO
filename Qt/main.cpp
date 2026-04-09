#include <QApplication>
#include "app.h"

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);
    a.setStyle("Fusion");

    QPalette pal;
    pal.setColor(QPalette::Window, QColor(Theme::BG));
    pal.setColor(QPalette::WindowText, QColor(Theme::TEXT_PRI));
    pal.setColor(QPalette::Base, QColor(Theme::BG));
    pal.setColor(QPalette::Text, QColor(Theme::TEXT_PRI));
    a.setPalette(pal);

    App w;
    w.show();
    return a.exec();
}
