
int main() {
    Rectangle rect(5, 3); 
    std::cout << "Width: " << rect.getWidth() << std::endl;
    std::cout << "Height: " << rect.getHeight() << std::endl;
    std::cout << "Area of the rectangle: " << rect.area() << std::endl; 
    rect.setWidth(7);
    rect.setHeight(4); 
    std::cout << "Updated area of the rectangle: " << rect.area() << std::endl; 
    return 0;
}
