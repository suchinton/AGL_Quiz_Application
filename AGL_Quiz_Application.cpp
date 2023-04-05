#include <QApplication>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QLabel label("Hello, This is Suchinton's Demo App!");
    label.setAlignment(Qt::AlignCenter);
    label.setStyleSheet("font-size: 20pt;");
    QVBoxLayout layout;
    layout.addWidget(&label);

    QPushButton button("Test Button");
    QObject::connect(&button, &QPushButton::clicked, [](){
        qDebug() << "This is a test button";
    });
    layout.addWidget(&button);

    QWidget window;
    window.setLayout(&layout);
    window.show();

    return app.exec();
}