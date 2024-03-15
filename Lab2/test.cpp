#include <iostream>
class Rectangle {
private:
    int width;
    int height;
public:
    Rectangle(int w, int h){}
    void setWidth(int w = 4) { width = w; }
    void setHeight(int h) { height = h; }
};
int main() {
    Rectangle rect(5, 3); 
    std::cout << "Width: " << rect.getWidth() << std::endl;
    std::cout << "Height: " << rect.getHeight() << std::endl;
    std::cout << "Area of the rectangle: " << rect.area() << std::endl;
    rect.setWidth();
    rect.setHeight(4);
    std::cout << "Updated area of the rectangle: " << rect.area() << std::endl;
    return 0;
}
