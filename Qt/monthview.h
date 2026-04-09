#pragma once
#include <QWidget>
#include <QLabel>
#include <QGridLayout>

class App;

class MonthView : public QWidget {
    Q_OBJECT
public:
    explicit MonthView(App *app);
    void rebuildCalendar();

private:
    void changeMonth(int delta);

    App *app;
    int currentYear;
    int currentMonth;
    QLabel *monthLabel;
    QWidget *calendarWidget;
    QVBoxLayout *mainLayout;
};
