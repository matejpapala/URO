#include "monthview.h"
#include "app.h"
#include <QHBoxLayout>
#include <QPushButton>
#include <QDate>
#include <QFrame>
#include <QLocale>

MonthView::MonthView(App *app) : QWidget(app), app(app) {
    QDate today = QDate::currentDate();
    currentYear = today.year();
    currentMonth = today.month();

    mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);

    auto *topBar = new QWidget;
    topBar->setFixedHeight(60);
    topBar->setStyleSheet(QString("background-color: %1;").arg(Theme::BG));
    auto *topLay = new QHBoxLayout(topBar);
    topLay->setContentsMargins(20, 0, 20, 0);

    auto *title = new QLabel(QString::fromUtf8("\xF0\x9F\x97\x93\xEF\xB8\x8F EVENT PLANNER"));
    title->setStyleSheet(QString("color: %1; font-size: 14px; font-weight: bold;").arg(Theme::TEXT_SEC));
    topLay->addWidget(title);
    topLay->addStretch();

    auto *addBtn = new QPushButton("+");
    addBtn->setFixedSize(40, 40);
    addBtn->setCursor(Qt::PointingHandCursor);
    addBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; font-size: 24px; border: none; }"
        "QPushButton:hover { background-color: %2; }"
    ).arg(Theme::TEXT_PRI, Theme::BG_SEC));
    connect(addBtn, &QPushButton::clicked, app, &App::showAddEvent);
    topLay->addWidget(addBtn);

    mainLayout->addWidget(topBar);

    auto *sep = new QFrame;
    sep->setFixedHeight(1);
    sep->setStyleSheet(QString("background-color: %1;").arg(Theme::BORDER));
    mainLayout->addWidget(sep);

    auto *monthSel = new QWidget;
    monthSel->setFixedHeight(80);
    auto *mLay = new QHBoxLayout(monthSel);

    auto *prevBtn = new QPushButton("<");
    prevBtn->setFixedSize(30, 30);
    prevBtn->setCursor(Qt::PointingHandCursor);
    prevBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; font-size: 18px; border: none; }"
        "QPushButton:hover { color: %2; }"
    ).arg(Theme::TEXT_SEC, Theme::TEXT_PRI));
    connect(prevBtn, &QPushButton::clicked, this, [this]{ changeMonth(-1); });

    monthLabel = new QLabel;
    monthLabel->setAlignment(Qt::AlignCenter);
    monthLabel->setStyleSheet(QString("color: %1; font-size: 20px; font-weight: bold;").arg(Theme::TEXT_PRI));

    auto *nextBtn = new QPushButton(">");
    nextBtn->setFixedSize(30, 30);
    nextBtn->setCursor(Qt::PointingHandCursor);
    nextBtn->setStyleSheet(prevBtn->styleSheet());
    connect(nextBtn, &QPushButton::clicked, this, [this]{ changeMonth(1); });

    mLay->addStretch();
    mLay->addWidget(prevBtn);
    mLay->addSpacing(20);
    mLay->addWidget(monthLabel);
    mLay->addSpacing(20);
    mLay->addWidget(nextBtn);
    mLay->addStretch();

    mainLayout->addWidget(monthSel);

    calendarWidget = nullptr;

    rebuildCalendar();
}

void MonthView::changeMonth(int delta) {
    currentMonth += delta;
    if (currentMonth > 12) { currentMonth = 1; currentYear++; }
    else if (currentMonth < 1) { currentMonth = 12; currentYear--; }
    rebuildCalendar();
}

void MonthView::rebuildCalendar() {
    if (calendarWidget) {
        mainLayout->removeWidget(calendarWidget);
        delete calendarWidget;
    }

    QString monthName = QLocale::c().monthName(currentMonth).toUpper();
    QString spaced;
    for (int i = 0; i < monthName.size(); i++) {
        if (i > 0) spaced += ' ';
        spaced += monthName[i];
    }
    monthLabel->setText(QString("%1   %2").arg(spaced).arg(currentYear));

    calendarWidget = new QWidget;
    calendarWidget->setStyleSheet(QString("background-color: %1;").arg(Theme::BORDER));
    auto *grid = new QGridLayout(calendarWidget);
    grid->setSpacing(1);
    grid->setContentsMargins(1, 1, 1, 1);

    mainLayout->addWidget(calendarWidget, 1);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    calendarWidget->setContentsMargins(40, 0, 40, 40);

    const char *days[] = {"MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"};
    for (int i = 0; i < 7; i++) {
        grid->setColumnStretch(i, 1);
        auto *cell = new QWidget;
        cell->setFixedHeight(40);
        cell->setStyleSheet(QString("background-color: %1;").arg(Theme::BG));
        auto *lay = new QVBoxLayout(cell);
        lay->setContentsMargins(0, 0, 0, 0);
        auto *lbl = new QLabel(days[i]);
        lbl->setAlignment(Qt::AlignCenter);
        lbl->setStyleSheet(QString("color: %1; font-size: 12px; font-weight: bold; background: transparent;").arg(Theme::TEXT_SEC));
        lay->addWidget(lbl);
        grid->addWidget(cell, 0, i);
    }

    QDate firstOfMonth(currentYear, currentMonth, 1);
    int startCol = firstOfMonth.dayOfWeek() - 1;
    int numDays = firstOfMonth.daysInMonth();

    int dayCounter = 1;
    for (int row = 1; row <= 6; row++) {
        grid->setRowStretch(row, 1);
        for (int col = 0; col < 7; col++) {
            auto *cell = new QWidget;
            cell->setStyleSheet(QString("background-color: %1;").arg(Theme::BG));
            auto *cellLay = new QVBoxLayout(cell);
            cellLay->setContentsMargins(10, 10, 10, 10);
            cellLay->setSpacing(0);

            if ((row == 1 && col < startCol) || dayCounter > numDays) {
                grid->addWidget(cell, row, col);
                continue;
            }

            auto *dayLbl = new QLabel(QString::number(dayCounter));
            dayLbl->setStyleSheet(QString("color: %1; font-size: 14px; background: transparent;").arg(Theme::TEXT_PRI));
            cellLay->addWidget(dayLbl, 0, Qt::AlignTop | Qt::AlignLeft);

            QString dateKey = QDate(currentYear, currentMonth, dayCounter).toString("yyyy-MM-dd");
            if (app->events.contains(dateKey)) {
                QString name = app->events[dateKey];
                if (name.size() > 12) name = name.left(12) + "..";

                cellLay->addStretch();
                auto *evLbl = new QLabel(QString::fromUtf8("\u25CF ") + name.toUpper());
                evLbl->setStyleSheet(QString("color: %1; font-size: 10px; font-weight: bold; background: transparent;").arg(Theme::ACCENT));
                evLbl->setCursor(Qt::PointingHandCursor);
                cellLay->addWidget(evLbl, 0, Qt::AlignBottom | Qt::AlignLeft);

                cell->setCursor(Qt::PointingHandCursor);
                auto clickHandler = [this, dateKey]() { app->showEventDetails(dateKey); };
                auto *overlay = new QPushButton(cell);
                overlay->setStyleSheet("background: transparent; border: none;");
                overlay->setCursor(Qt::PointingHandCursor);
                overlay->setGeometry(0, 0, 9999, 9999);
                overlay->lower();
                overlay->raise();
                overlay->setFlat(true);
                connect(overlay, &QPushButton::clicked, this, clickHandler);
            }

            cellLay->addStretch();
            grid->addWidget(cell, row, col);
            dayCounter++;
        }
        if (dayCounter > numDays) break;
    }
}
