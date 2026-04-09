#include "addeventview.h"
#include "app.h"
#include "datepickerpopup.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QFrame>

AddEventView::AddEventView(App *app) : QWidget(app), app(app) {
    auto *mainLay = new QVBoxLayout(this);
    mainLay->setContentsMargins(0, 0, 0, 0);
    mainLay->setSpacing(0);

    auto *topBar = new QWidget;
    topBar->setFixedHeight(60);
    topBar->setStyleSheet(QString("background-color: %1;").arg(Theme::BG));
    auto *topLay = new QHBoxLayout(topBar);
    topLay->setContentsMargins(20, 0, 20, 0);
    auto *title = new QLabel(QString::fromUtf8("\xF0\x9F\x97\x93\xEF\xB8\x8F EVENT PLANNER"));
    title->setStyleSheet(QString("color: %1; font-size: 14px; font-weight: bold;").arg(Theme::TEXT_SEC));
    topLay->addWidget(title);
    topLay->addStretch();
    mainLay->addWidget(topBar);

    auto *sep = new QFrame;
    sep->setFixedHeight(1);
    sep->setStyleSheet(QString("background-color: %1;").arg(Theme::BORDER));
    mainLay->addWidget(sep);

    mainLay->addStretch();
    auto *content = new QWidget;
    content->setFixedWidth(500);
    auto *cLay = new QVBoxLayout(content);
    cLay->setSpacing(0);

    auto *heading = new QLabel("New Event");
    heading->setStyleSheet(QString("color: %1; font-size: 32px;").arg(Theme::TEXT_PRI));
    cLay->addWidget(heading);

    auto *accent = new QFrame;
    accent->setFixedSize(150, 2);
    accent->setStyleSheet(QString("background-color: %1;").arg(Theme::ACCENT));
    cLay->addWidget(accent);
    cLay->addSpacing(40);

    auto *nameLbl = new QLabel("EVENT NAME");
    nameLbl->setStyleSheet(QString("color: %1; font-size: 10px; font-weight: bold;").arg(Theme::TEXT_SEC));
    cLay->addWidget(nameLbl);

    nameInput = new QLineEdit;
    nameInput->setPlaceholderText("Untitled Gathering");
    nameInput->setStyleSheet(QString(
        "QLineEdit { background: transparent; color: %1; border: none; border-bottom: 1px solid %2; "
        "font-size: 16px; padding: 8px 0; }"
    ).arg(Theme::TEXT_PRI, Theme::BORDER));
    cLay->addWidget(nameInput);
    cLay->addSpacing(30);

    auto *dateLbl = new QLabel("DATE");
    dateLbl->setStyleSheet(QString("color: %1; font-size: 10px; font-weight: bold;").arg(Theme::TEXT_SEC));
    cLay->addWidget(dateLbl);

    auto *dateRow = new QWidget;
    auto *dateRowLay = new QHBoxLayout(dateRow);
    dateRowLay->setContentsMargins(0, 0, 0, 0);

    dateInput = new QLineEdit;
    dateInput->setPlaceholderText("YYYY - MM - DD");
    dateInput->setReadOnly(true);
    dateInput->setStyleSheet(QString(
        "QLineEdit { background: transparent; color: %1; border: none; border-bottom: 1px solid %2; "
        "font-size: 16px; padding: 8px 0; }"
    ).arg(Theme::TEXT_PRI, Theme::BORDER));
    dateRowLay->addWidget(dateInput);

    auto *calBtn = new QPushButton(QString::fromUtf8("\xF0\x9F\x93\x85"));
    calBtn->setFixedSize(40, 30);
    calBtn->setCursor(Qt::PointingHandCursor);
    calBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; font-size: 20px; border: none; }"
        "QPushButton:hover { background-color: %2; }"
    ).arg(Theme::ACCENT, Theme::BG_SEC));
    connect(calBtn, &QPushButton::clicked, this, &AddEventView::openDatePicker);
    dateRowLay->addWidget(calBtn);

    cLay->addWidget(dateRow);
    cLay->addSpacing(40);

    auto *btnFrame = new QWidget;
    auto *btnLay = new QHBoxLayout(btnFrame);
    btnLay->setContentsMargins(0, 0, 0, 0);
    btnLay->addStretch();

    auto *cancelBtn = new QPushButton("Cancel");
    cancelBtn->setCursor(Qt::PointingHandCursor);
    cancelBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; border: 1px solid %2; "
        "padding: 10px 30px; font-size: 12px; }"
        "QPushButton:hover { background-color: %2; }"
    ).arg(Theme::TEXT_PRI, Theme::BORDER));
    connect(cancelBtn, &QPushButton::clicked, app, &App::showMonthView);
    btnLay->addWidget(cancelBtn);

    auto *saveBtn = new QPushButton("SAVE EVENT");
    saveBtn->setCursor(Qt::PointingHandCursor);
    saveBtn->setStyleSheet(QString(
        "QPushButton { background-color: %1; color: white; border: none; "
        "padding: 10px 30px; font-size: 12px; font-weight: bold; }"
        "QPushButton:hover { background-color: #2d2ddb; }"
    ).arg(Theme::ACCENT));
    connect(saveBtn, &QPushButton::clicked, this, &AddEventView::saveEvent);
    btnLay->addWidget(saveBtn);

    cLay->addWidget(btnFrame);

    auto *centerLay = new QHBoxLayout;
    centerLay->addStretch();
    centerLay->addWidget(content);
    centerLay->addStretch();

    mainLay->addLayout(centerLay);
    mainLay->addStretch();
}

void AddEventView::reset() {
    nameInput->clear();
    dateInput->clear();
}

void AddEventView::openDatePicker() {
    auto *picker = new DatePickerPopup(this, dateInput->text());
    connect(picker, &DatePickerPopup::dateSelected, this, [this](const QString &d) {
        dateInput->setText(d);
    });
    picker->show();
}

void AddEventView::saveEvent() {
    QString name = nameInput->text().trimmed();
    QString date = dateInput->text().trimmed();
    if (!name.isEmpty() && !date.isEmpty()) {
        app->events[date] = name;
        reset();
        app->showMonthView();
    }
}
