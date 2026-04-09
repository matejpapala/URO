#include "app.h"
#include "monthview.h"
#include "addeventview.h"
#include "eventdetailsview.h"

App::App(QWidget *parent) : QMainWindow(parent) {
    setWindowTitle("Event Planner");
    resize(1000, 700);
    setStyleSheet(QString("QMainWindow { background-color: %1; }").arg(Theme::BG));

    QDate today = QDate::currentDate();
    QString testDate = QDate(today.year(), today.month(), 15).toString("yyyy-MM-dd");
    events[testDate] = "PAP0124";

    stack = new QStackedWidget(this);
    setCentralWidget(stack);

    monthView = new MonthView(this);
    addEventView = new AddEventView(this);
    eventDetailsView = new EventDetailsView(this);

    stack->addWidget(monthView);
    stack->addWidget(addEventView);
    stack->addWidget(eventDetailsView);

    showMonthView();
}

void App::showMonthView() {
    monthView->rebuildCalendar();
    stack->setCurrentWidget(monthView);
}

void App::showAddEvent() {
    addEventView->reset();
    stack->setCurrentWidget(addEventView);
}

void App::showEventDetails(const QString &dateKey) {
    eventDetailsView->loadEvent(dateKey);
    stack->setCurrentWidget(eventDetailsView);
}
