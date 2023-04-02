#include <QApplication>
#include <QLabel>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QLabel label("Hello, This is Suchinton's Demo App!");
    label.show();

    return app.exec();
}