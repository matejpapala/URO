#pragma once
#include <QWidget>
#include <QLineEdit>

class App;

class AddEventView : public QWidget {
    Q_OBJECT
public:
    explicit AddEventView(App *app);
    void reset();

private:
    void openDatePicker();
    void saveEvent();

    App *app;
    QLineEdit *nameInput;
    QLineEdit *dateInput;
};
