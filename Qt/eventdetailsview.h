#pragma once
#include <QWidget>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QStackedWidget>

class App;

class EventDetailsView : public QWidget {
    Q_OBJECT
public:
    explicit EventDetailsView(App *app);
    void loadEvent(const QString &dateKey);

private:
    void toggleEdit();
    void deleteEvent();
    void openDatePicker();

    App *app;
    QString currentDate;
    bool editing = false;

    QLabel *titleLabel;
    QLabel *subtitleLabel;

    QLabel *nameValueLabel;
    QLabel *dateValueLabel;

    QLineEdit *nameEdit;
    QLineEdit *dateEdit;

    QWidget *nameViewWidget;
    QWidget *nameEditWidget;
    QWidget *dateViewWidget;
    QWidget *dateEditWidget;

    QPushButton *editBtn;
};
