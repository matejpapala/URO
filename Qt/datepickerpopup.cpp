#include "datepickerpopup.h"
#include "app.h"
#include <QHBoxLayout>
#include <QPushButton>
#include <QDate>
#include <QLocale>

DatePickerPopup::DatePickerPopup(QWidget *parent, const QString &initialDate)
    : QDialog(parent, Qt::Popup) {
    setFixedSize(320, 350);
    setStyleSheet(QString("QDialog { background-color: %1; }").arg(Theme::BG));
    setWindowFlags(windowFlags() | Qt::WindowStaysOnTopHint);

    QDate init = QDate::fromString(initialDate, "yyyy-MM-dd");
    if (!init.isValid()) init = QDate::currentDate();
    currentYear = init.year();
    currentMonth = init.month();

    mainLay = new QVBoxLayout(this);
    mainLay->setContentsMargins(10, 10, 10, 10);

    auto *headerLay = new QHBoxLayout;
    auto *prevBtn = new QPushButton("<");
    prevBtn->setFixedSize(30, 30);
    prevBtn->setCursor(Qt::PointingHandCursor);
    prevBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; border: none; }"
        "QPushButton:hover { background-color: %2; }"
    ).arg(Theme::TEXT_PRI, Theme::BG_SEC));
    connect(prevBtn, &QPushButton::clicked, this, &DatePickerPopup::prevMonth);

    monthLabel = new QLabel;
    monthLabel->setAlignment(Qt::AlignCenter);
    monthLabel->setStyleSheet(QString("color: %1; font-size: 16px; font-weight: bold;").arg(Theme::TEXT_PRI));

    auto *nextBtn = new QPushButton(">");
    nextBtn->setFixedSize(30, 30);
    nextBtn->setCursor(Qt::PointingHandCursor);
    nextBtn->setStyleSheet(prevBtn->styleSheet());
    connect(nextBtn, &QPushButton::clicked, this, &DatePickerPopup::nextMonth);

    headerLay->addWidget(prevBtn);
    headerLay->addStretch();
    headerLay->addWidget(monthLabel);
    headerLay->addStretch();
    headerLay->addWidget(nextBtn);
    mainLay->addLayout(headerLay);

    auto *dayHeaderWidget = new QWidget;
    auto *dayHeaderLay = new QGridLayout(dayHeaderWidget);
    dayHeaderLay->setSpacing(2);
    const char *days[] = {"Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"};
    for (int i = 0; i < 7; i++) {
        dayHeaderLay->setColumnStretch(i, 1);
        auto *lbl = new QLabel(days[i]);
        lbl->setAlignment(Qt::AlignCenter);
        lbl->setStyleSheet(QString("color: %1; font-size: 12px; font-weight: bold;").arg(Theme::TEXT_SEC));
        dayHeaderLay->addWidget(lbl, 0, i);
    }
    mainLay->addWidget(dayHeaderWidget);

    daysWidget = nullptr;
    buildCalendar();
}

void DatePickerPopup::prevMonth() {
    if (currentMonth == 1) { currentMonth = 12; currentYear--; }
    else currentMonth--;
    buildCalendar();
}

void DatePickerPopup::nextMonth() {
    if (currentMonth == 12) { currentMonth = 1; currentYear++; }
    else currentMonth++;
    buildCalendar();
}

void DatePickerPopup::buildCalendar() {
    if (daysWidget) {
        mainLay->removeWidget(daysWidget);
        delete daysWidget;
    }

    QString name = QLocale::c().monthName(currentMonth);
    monthLabel->setText(QString("%1 %2").arg(name).arg(currentYear));

    daysWidget = new QWidget;
    daysGrid = new QGridLayout(daysWidget);
    daysGrid->setSpacing(2);

    QDate first(currentYear, currentMonth, 1);
    int startCol = first.dayOfWeek() - 1;
    int numDays = first.daysInMonth();

    int dayCounter = 1;
    for (int row = 0; row < 6; row++) {
        for (int col = 0; col < 7; col++) {
            daysGrid->setColumnStretch(col, 1);
            if ((row == 0 && col < startCol) || dayCounter > numDays) continue;

            auto *btn = new QPushButton(QString::number(dayCounter));
            btn->setFixedSize(35, 35);
            btn->setCursor(Qt::PointingHandCursor);
            btn->setStyleSheet(QString(
                "QPushButton { background: transparent; color: %1; border: none; font-size: 13px; }"
                "QPushButton:hover { background-color: %2; }"
            ).arg(Theme::TEXT_PRI, Theme::BG_SEC));
            connect(btn, &QPushButton::clicked, this, [this, d=dayCounter]{ selectDate(d); });
            daysGrid->addWidget(btn, row, col, Qt::AlignCenter);
            dayCounter++;
        }
        if (dayCounter > numDays) break;
    }

    mainLay->addWidget(daysWidget, 1);
}

void DatePickerPopup::selectDate(int day) {
    QString dateStr = QDate(currentYear, currentMonth, day).toString("yyyy-MM-dd");
    emit dateSelected(dateStr);
    close();
}
