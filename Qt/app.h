#pragma once
#include <QMainWindow>
#include <QStackedWidget>
#include <QMap>
#include <QString>
#include <QDate>

class MonthView;
class AddEventView;
class EventDetailsView;

namespace Theme {
    constexpr auto BG         = "#1c1c1c";
    constexpr auto BG_SEC     = "#404040";
    constexpr auto ACCENT     = "#3c3cf6";
    constexpr auto TEXT_PRI   = "#ffffff";
    constexpr auto TEXT_SEC   = "#94a3b8";
    constexpr auto BORDER     = "#404040";
}

class App : public QMainWindow {
    Q_OBJECT
public:
    explicit App(QWidget *parent = nullptr);

    QMap<QString, QString> events;

    void showMonthView();
    void showAddEvent();
    void showEventDetails(const QString &dateKey);

private:
    QStackedWidget *stack;
    MonthView      *monthView;
    AddEventView   *addEventView;
    EventDetailsView *eventDetailsView;
};
