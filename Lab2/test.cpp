#include <iostream>

int main() {
    int arr[] = {64, 25, 12, 22, 11};
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
		}
        }
    }
    std::cout << "Sorted array: " << std::endl;
    for (int i = 0; i < n; ++i) {
        std::cout << arr[i] << std::endl;
    }
    std::cout << std::endl;
    return 0;
}
