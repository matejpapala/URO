#include "eventdetailsview.h"
#include "app.h"
#include "datepickerpopup.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFrame>
#include <QDate>

EventDetailsView::EventDetailsView(App *app) : QWidget(app), app(app) {
    auto *outer = new QVBoxLayout(this);
    outer->setContentsMargins(150, 100, 150, 100);

    auto *header = new QHBoxLayout;
    auto *headerLbl = new QLabel(QString::fromUtf8("\xF0\x9F\x97\x93\xEF\xB8\x8F Event Details"));
    headerLbl->setStyleSheet(QString("color: %1; font-size: 16px; font-weight: bold;").arg(Theme::TEXT_PRI));
    header->addWidget(headerLbl);
    header->addStretch();

    auto *deleteBtn = new QPushButton(QString::fromUtf8("\xF0\x9F\x97\x91"));
    deleteBtn->setFixedSize(30, 30);
    deleteBtn->setCursor(Qt::PointingHandCursor);
    deleteBtn->setStyleSheet(QString(
        "QPushButton { background-color: %1; color: %2; font-size: 18px; border: none; }"
        "QPushButton:hover { background-color: %3; }"
    ).arg(Theme::BG_SEC, Theme::ACCENT, Theme::BORDER));
    connect(deleteBtn, &QPushButton::clicked, this, &EventDetailsView::deleteEvent);
    header->addWidget(deleteBtn);
    outer->addLayout(header);

    auto *sep1 = new QFrame;
    sep1->setFixedHeight(1);
    sep1->setStyleSheet(QString("background-color: %1;").arg(Theme::BORDER));
    outer->addWidget(sep1);
    outer->addSpacing(30);

    titleLabel = new QLabel;
    titleLabel->setStyleSheet(QString("color: %1; font-size: 42px; font-weight: bold;").arg(Theme::TEXT_PRI));
    outer->addWidget(titleLabel);

    subtitleLabel = new QLabel;
    subtitleLabel->setStyleSheet(QString("color: %1; font-size: 16px;").arg(Theme::TEXT_SEC));
    outer->addWidget(subtitleLabel);
    outer->addSpacing(30);

    auto *sep2 = new QFrame;
    sep2->setFixedHeight(1);
    sep2->setStyleSheet(QString("background-color: %1;").arg(Theme::BORDER));
    outer->addWidget(sep2);

    auto *nameRow = new QHBoxLayout;
    auto *nameLbl = new QLabel("EVENT NAME");
    nameLbl->setFixedWidth(200);
    nameLbl->setStyleSheet(QString("color: %1; font-size: 12px;").arg(Theme::TEXT_SEC));
    nameRow->addWidget(nameLbl);

    nameValueLabel = new QLabel;
    nameValueLabel->setStyleSheet(QString("color: %1; font-size: 14px;").arg(Theme::TEXT_PRI));
    nameEdit = new QLineEdit;
    nameEdit->setStyleSheet(QString(
        "QLineEdit { background: transparent; color: %1; border: none; border-bottom: 1px solid %2; "
        "font-size: 14px; padding: 4px 0; }"
    ).arg(Theme::TEXT_PRI, Theme::BORDER));
    nameEdit->hide();

    nameRow->addWidget(nameValueLabel);
    nameRow->addWidget(nameEdit);
    nameRow->addStretch();
    outer->addLayout(nameRow);

    auto *sep3 = new QFrame;
    sep3->setFixedHeight(1);
    sep3->setStyleSheet(QString("background-color: %1;").arg(Theme::BORDER));
    outer->addWidget(sep3);

    auto *dateRow = new QHBoxLayout;
    auto *dateLbl = new QLabel("EVENT DATE");
    dateLbl->setFixedWidth(200);
    dateLbl->setStyleSheet(QString("color: %1; font-size: 12px;").arg(Theme::TEXT_SEC));
    dateRow->addWidget(dateLbl);

    dateValueLabel = new QLabel;
    dateValueLabel->setStyleSheet(QString("color: %1; font-size: 14px;").arg(Theme::TEXT_PRI));

    dateEdit = new QLineEdit;
    dateEdit->setReadOnly(true);
    dateEdit->setStyleSheet(nameEdit->styleSheet());
    dateEdit->hide();

    auto *dateCalBtn = new QPushButton(QString::fromUtf8("\xF0\x9F\x93\x85"));
    dateCalBtn->setFixedSize(30, 30);
    dateCalBtn->setCursor(Qt::PointingHandCursor);
    dateCalBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; font-size: 16px; border: none; }"
    ).arg(Theme::ACCENT));
    dateCalBtn->hide();
    connect(dateCalBtn, &QPushButton::clicked, this, &EventDetailsView::openDatePicker);

    dateRow->addWidget(dateValueLabel);
    dateRow->addWidget(dateEdit);
    dateRow->addWidget(dateCalBtn);
    dateRow->addStretch();
    outer->addLayout(dateRow);

    this->setProperty("dateCalBtn", QVariant::fromValue(static_cast<QObject*>(dateCalBtn)));

    outer->addSpacing(50);

    auto *btnLay = new QHBoxLayout;
    editBtn = new QPushButton("Edit Details");
    editBtn->setCursor(Qt::PointingHandCursor);
    editBtn->setStyleSheet(QString(
        "QPushButton { background-color: %1; color: white; border: none; "
        "padding: 10px 30px; font-size: 14px; font-weight: bold; }"
        "QPushButton:hover { background-color: #2d2ddb; }"
    ).arg(Theme::ACCENT));
    connect(editBtn, &QPushButton::clicked, this, &EventDetailsView::toggleEdit);
    btnLay->addWidget(editBtn);

    auto *cancelBtn = new QPushButton("Cancel");
    cancelBtn->setCursor(Qt::PointingHandCursor);
    cancelBtn->setStyleSheet(QString(
        "QPushButton { background: transparent; color: %1; border: 1px solid %2; "
        "padding: 10px 30px; font-size: 14px; }"
        "QPushButton:hover { background-color: %2; }"
    ).arg(Theme::TEXT_PRI, Theme::BORDER));
    connect(cancelBtn, &QPushButton::clicked, app, &App::showMonthView);
    btnLay->addWidget(cancelBtn);
    btnLay->addStretch();
    outer->addLayout(btnLay);

    outer->addStretch();
}

void EventDetailsView::loadEvent(const QString &dateKey) {
    currentDate = dateKey;
    QString name = app->events.value(dateKey);

    titleLabel->setText(name);

    QDate d = QDate::fromString(dateKey, "yyyy-MM-dd");
    QString formatted = d.toString("MMMM d, yyyy");
    subtitleLabel->setText("Scheduled for " + formatted);

    nameValueLabel->setText(name);
    dateValueLabel->setText(formatted);

    if (editing) toggleEdit();
}

void EventDetailsView::toggleEdit() {
    editing = !editing;
    auto *dateCalBtn = qobject_cast<QPushButton*>(property("dateCalBtn").value<QObject*>());

    if (editing) {
        editBtn->setText("Save Changes");
        nameValueLabel->hide();
        dateValueLabel->hide();
        nameEdit->setText(nameValueLabel->text());
        nameEdit->show();
        dateEdit->setText(currentDate);
        dateEdit->show();
        if (dateCalBtn) dateCalBtn->show();
    } else {
        QString newName = nameEdit->text().trimmed();
        QString newDate = dateEdit->text().trimmed();

        if (!newName.isEmpty() && !newDate.isEmpty()) {
            if (currentDate != newDate)
                app->events.remove(currentDate);
            app->events[newDate] = newName;
            currentDate = newDate;
        }

        editBtn->setText("Edit Details");
        nameEdit->hide();
        dateEdit->hide();
        if (dateCalBtn) dateCalBtn->hide();

        loadEvent(currentDate);
        nameValueLabel->show();
        dateValueLabel->show();
    }
}

void EventDetailsView::deleteEvent() {
    app->events.remove(currentDate);
    app->showMonthView();
}

void EventDetailsView::openDatePicker() {
    auto *picker = new DatePickerPopup(this, dateEdit->text());
    connect(picker, &DatePickerPopup::dateSelected, this, [this](const QString &d) {
        dateEdit->setText(d);
    });
    picker->show();
}
