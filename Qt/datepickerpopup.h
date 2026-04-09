#pragma once
#include <QDialog>
#include <QLabel>
#include <QGridLayout>

class DatePickerPopup : public QDialog {
    Q_OBJECT
public:
    explicit DatePickerPopup(QWidget *parent, const QString &initialDate = QString());

signals:
    void dateSelected(const QString &date);

private:
    void prevMonth();
    void nextMonth();
    void buildCalendar();
    void selectDate(int day);

    int currentYear;
    int currentMonth;
    QLabel *monthLabel;
    QGridLayout *daysGrid;
    QWidget *daysWidget;
    QVBoxLayout *mainLay;
};
